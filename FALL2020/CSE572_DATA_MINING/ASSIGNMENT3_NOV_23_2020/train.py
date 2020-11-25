import sys
from datetime import datetime  # , date, time
from functools import wraps
from math import ceil

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis, entropy
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.cluster import contingency_matrix

MIN30 = pd.Timedelta(minutes=30)
HOURS2 = pd.Timedelta(hours=2)

CGM_USECOLS = ["Date", "Time", "Sensor Glucose (mg/dL)"]
INSULIN_USECOLS = ["Date", "Time", "BWZ Carb Input (grams)"]

BIN_SIZE = 20


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'[{datetime.now()}] {f.__name__} started')
        try:
            return f(*args, **kwargs)
        finally:
            print(f'[{datetime.now()}] {f.__name__} completed')

    return wrapper


@timer
def extract_datetimes(df):
    datetimes = df[['Date', 'Time']]
    # res = []
    # for _, (d, t) in datetimes.iterrows():
    #     month, day, year = map(int, d.split('/'))
    #     hour, minute, second = map(int, t.split(':'))
    #     res.append(datetime.combine(date(year, month, day), time(hour, minute, second)))
    #
    # return res
    datetimes = [f'{d} {t}' for _, (d, t) in datetimes.iterrows()]
    return pd.to_datetime(datetimes)  # , format='%m/%d/%Y %H:%M:%S')


@timer
def preprocess_df_cgm(df_cgm):
    df_cgm = df_cgm.iloc[::-1]
    df_cgm['Sensor Glucose (mg/dL)'].interpolate(inplace=True)
    df_cgm['DateTime'] = extract_datetimes(df_cgm)
    return df_cgm


@timer
def preprocess_df_insulin(df_insulin):
    df_insulin = df_insulin.iloc[::-1]
    df_insulin['DateTime'] = extract_datetimes(df_insulin)
    return df_insulin


@timer
def get_meals(df_cgm, df_insulin):
    meal_timestamps = df_insulin[df_insulin['BWZ Carb Input (grams)'].notna()]['DateTime'].tolist()
    carb_inputs = df_insulin[df_insulin['BWZ Carb Input (grams)'].notna()]['BWZ Carb Input (grams)'].tolist()

    list_meals = []
    list_carb_inputs = []
    i = 0
    while i < len(meal_timestamps):
        while i + 1 < len(meal_timestamps) and meal_timestamps[i + 1] < meal_timestamps[i] + HOURS2:
            i += 1
        start = meal_timestamps[i] - MIN30
        end = meal_timestamps[i] + HOURS2

        cgm_timespan = df_cgm[(start <= df_cgm["DateTime"]) & (df_cgm["DateTime"] <= end)]
        cgm = cgm_timespan["Sensor Glucose (mg/dL)"].tolist()

        if len(cgm) == 30:
            list_meals.append(cgm)
            list_carb_inputs.append(carb_inputs[i])
        i += 1

    return list_meals, list_carb_inputs


def extract_features(fcgm):
    fcgm = np.array(fcgm)

    velocity = np.gradient(fcgm)
    velocity_index = velocity.argmax()
    max_velocity = velocity[velocity_index]

    return [
        fcgm.argmax() - fcgm.argmin(),
        abs(fcgm.max()) - abs(fcgm.min()),
        np.gradient(fcgm).max(),
        max_velocity,
        velocity_index,
        np.sqrt((fcgm ** 2).mean()),
        fcgm.mean(),
        fcgm.std(),
        skew(fcgm),
        kurtosis(fcgm)
    ]


binnumber = lambda carbs, mincarbs: max(ceil((carbs - mincarbs) / BIN_SIZE) - 1, 0)


def load_df(filename, usecols):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, usecols=usecols)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filename, sheet_name='Sheet1', usecols=usecols)
    raise Exception('Only csv and xlsx inputs are supported')


def purity_score(ground_truth, labels):
    # compute contingency matrix (also called confusion matrix)
    cont_mat = contingency_matrix(ground_truth, labels)
    # return purity
    return np.sum(np.amax(cont_mat, axis=0)) / np.sum(cont_mat)


def sse_score(X, labels):
    sse = 0
    for i in range(n):
        cluster = X[labels == i]
        mean = cluster.mean(axis=0)
        sse += ((cluster - mean) ** 2).sum()
    return sse


def entropy_score(ground_truth, labels, n):
    ent = 0
    for i in range(n):
        bincount = np.bincount(ground_truth[labels == i])
        w = (labels == i).sum()
        probabilities = bincount[bincount != 0] / w
        ent += entropy(probabilities) * w / labels.shape[0]
    return ent


if __name__ == '__main__':
    # Given: 	Meal Data of 2 subjects
    try:
        insulin_filename = sys.argv[1]
        df_filename = sys.argv[2]
    except IndexError:
        print(f'[Usage] python InsulinData.csv CGMData.csv')
        exit()

    df_insulin = load_df(insulin_filename, INSULIN_USECOLS)
    df_cgm = load_df(df_filename, CGM_USECOLS)

    df_insulin = preprocess_df_insulin(df_insulin)
    df_cgm = preprocess_df_cgm(df_cgm)

    list_meals, list_carb_inputs = get_meals(df_cgm, df_insulin)

    X = list(map(extract_features, list_meals))
    X = np.array(X)
    # X = (X - X.mean()) / X.std()

    # Derive the max and min value of meal intake amount from the Y column of the Insulin data.
    maxcarbs = df_insulin['BWZ Carb Input (grams)'].max()
    mincarbs = df_insulin['BWZ Carb Input (grams)'].min()

    # Discretize the meal amount in bins of size 20.
    n = ceil((maxcarbs - mincarbs) / BIN_SIZE)
    ground_truth = [binnumber(carbs, mincarbs) for carbs in list_carb_inputs]
    ground_truth = np.array(ground_truth)

    # Performing clustering:
    # DBSCAN
    dbscan = DBSCAN(9.09, 3)
    dbscan.fit(X)
    labels = dbscan.labels_.tolist()
    for i in range(len(labels)):
        if labels[i] == -1:
            d = float('inf')
            l = -1
            for j in range(len(labels)):
                if dbscan.labels_[j] != -1:
                    nd = np.linalg.norm(X[i] - X[j])
                    if nd < d:
                        d = nd
                        l = dbscan.labels_[j]
            labels[i] = l
    dbscan.labels_ = np.array(labels)

    # KMeans
    kmeans = KMeans(n)
    kmeans.fit(X)

    # Report your accuracy of clustering based on SSE, entropy and purity metrics.
    cols = ['SSE', 'Entropy', 'Purity']
    rows = [
        [sse_score(X, dbscan.labels_), entropy_score(ground_truth, dbscan.labels_, n),
         purity_score(ground_truth, dbscan.labels_)],
        [sse_score(X, kmeans.labels_), entropy_score(ground_truth, kmeans.labels_, n),
         purity_score(ground_truth, kmeans.labels_)],
    ]
    df = pd.DataFrame(rows, columns=cols, index=['DBScan', 'KMeans'])
    print(df)
