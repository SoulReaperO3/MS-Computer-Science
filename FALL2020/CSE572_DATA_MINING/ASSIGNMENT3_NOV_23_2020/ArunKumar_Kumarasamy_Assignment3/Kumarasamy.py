#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.fftpack
from sklearn.decomposition import PCA
from math import log2
from sklearn.cluster import KMeans,DBSCAN

print("=====================Started===========================")
#load Insulin and CGM Data
insulinDf = pd.read_csv('InsulinData.csv', parse_dates=[['Date','Time']],low_memory=False).iloc[::-1]
cgmDf = pd.read_csv('CGMData.csv', parse_dates=[['Date','Time']],low_memory=False).iloc[::-1]

insulinDFColY = insulinDf[insulinDf['BWZ Carb Input (grams)'].notnull() & insulinDf['BWZ Carb Input (grams)'] != 0]
insulinMealDates = pd.DataFrame(insulinDFColY[['Date_Time','BWZ Carb Input (grams)']])

insulinMealDates['Diff'] = insulinMealDates.iloc[:,0].diff(-1).dt.total_seconds().div(3600)
insulinMealDates = insulinMealDates.loc[insulinMealDates['Diff'] <= -2]
insulinMealDates.drop(insulinMealDates.head(1).index,inplace=True)
insulinMealDates.drop(insulinMealDates.tail(2).index,inplace=True)

binLen = 20
minV = insulinMealDates['BWZ Carb Input (grams)'].min()
maxV = insulinMealDates['BWZ Carb Input (grams)'].max()

nBins = (int)((maxV - minV)/20)

for ind in insulinMealDates.index:
    insulinMealDates['BWZ Carb Input (grams)'][ind] = (int)(insulinMealDates['BWZ Carb Input (grams)'][ind]/(minV + 20))
#     23,43,63,83,103,123,

mealDatesList = []
for ind in insulinMealDates.index: 
    l = []
    l.append((cgmDf.loc[cgmDf['Date_Time'] >= insulinMealDates['Date_Time'][ind]])['Date_Time'].iloc[0])
    l.append(insulinMealDates['BWZ Carb Input (grams)'][ind])
    mealDatesList.append(l)

mealDataMatrix = []
for mealDateTime in mealDatesList:
    idx = cgmDf[cgmDf['Date_Time'] == mealDateTime[0]]['Sensor Glucose (mg/dL)'].index[0]
    l = list(cgmDf['Sensor Glucose (mg/dL)'].iloc[cgmDf.shape[0]-1-idx-6:cgmDf.shape[0]-1-idx+24].values)
    l.append(mealDateTime[1])
    mealDataMatrix.append(l)

mealDf = pd.DataFrame(mealDataMatrix).dropna()
mealDf = mealDf.reset_index(drop=True)

#Extract cgm velocity
def extract_cgm_velocity(df, result_df):
  velocityDF = pd.DataFrame()
  for i in range(0,df.shape[1]-5):
      velocityDF['Vel_'+str(i)] = (df.iloc[:,i+5]-df.iloc[:,i])
  result_df['Window_Velocity_Max']=velocityDF.max(axis = 1, skipna=True)

#Extract cgm trend
def extract_cgm_trend(df, result_df):
    lunch = [[]]
    means = []
    for i in range(1, len(df)):
        lunch.append(df.iloc[i])
    for i in range(0, len(lunch)):
        means.append(df.iloc[i].mean())
    countmaster = []
    for i in range(0, len(lunch)):
        count = 0
        for j in df.iloc[i]:
            if j < means[i]:    
                count += 1
        countmaster.append(count)
    percentage=[]
    for i in countmaster:
        percentage.append((i / len(df.iloc[0])) * 100)
    result_df['cgmTrend'] = np.asarray(percentage)

#Extract Accelaration
def extract_acceleration(df, result_df):
    d=[]
    q=[]
    f=[]
    acc = [[],[],[],[]]
    for j in range(0, df.shape[0]):
        b = df.iloc[j]
        d = []
        for i in range(len(b)):
            if(np.isnan(b[i])):
                continue
            else:
                d.append(b[i])

        if(len(d) >= 1):
            solar_elevation_angle_1stdev = np.gradient(d)
            solar_elevation_angle_2nddev = np.gradient(solar_elevation_angle_1stdev)

            q = solar_elevation_angle_2nddev
            arr = q[5:10]
            acc[0].append(np.mean(arr))
            arr = q[10:15]
            acc[1].append(np.mean(arr))
            arr = q[15:20]
            acc[2].append(np.mean(arr))
            arr = q[20:25]
            acc[3].append(np.mean(arr))

        else:
            for i in range(4):
              acc[i].append(0)
    for i in range(4):
      result_df['acc'+str(i+1)] = acc[i]

#Extract entropy
def get_entropy(series):
    series_counts = series.value_counts()
    entropy = scipy.stats.entropy(series_counts)  
    return entropy

def extract_entropy(df, result_df):
    result_df['Entropy'] = df.apply(lambda row: get_entropy(row), axis=1)

#Extract Windowed mean
def extract_windowed_mean(df, result_df):
  if(df.shape[1] > 24):
    for i in range(6,df.shape[1],6):
      result_df['Mean_'+str(i-6)] = df.iloc[:,i:i+6].mean(axis = 1)
  else:
    for i in range(0,df.shape[1],6):
      result_df['Mean_'+str(i)] = df.iloc[:,i:i+6].mean(axis = 1)

# FFT- Finding top 8 values for each row
from numpy.fft import fft
def get_fft(row):
    cgmFFTValues = np.abs(fft(row))
    cgmFFTValues.sort()
    return np.flip(cgmFFTValues)[0:8]

def extract_fft(df, result_df):
  FFT = pd.DataFrame()
  FFT['FFT_Top2'] = df.apply(lambda row: get_fft(row), axis=1)
  FFT_updated = pd.DataFrame(FFT.FFT_Top2.tolist(), columns=['FFT_1', 'FFT_2', 'FFT_3', 'FFT_4', 'FFT_5', 'FFT_6', 'FFT_7', 'FFT_8'])
  FFT_updated.head()
  for i in range(8):
    result_df['FFT_'+str(i+1)] = FFT_updated['FFT_'+str(i+1)]
    
#get MinMaxDiff for each row
def get_minMaxDiff(series):
    return series.max() - series.min()
    
#Extract MinMaxDiff
def extract_minMaxDiff(df, result_df):
    result_df['MinMaxDifference']= df.apply(lambda row: get_minMaxDiff(row), axis=1)   

#1. Feature extraction
meal_features = pd.DataFrame()
result_dffft = pd.DataFrame()

def extract_features(data, result_df):
    extract_minMaxDiff(data, result_df)
    extract_cgm_velocity(data, result_df)
    extract_windowed_mean(data, result_df)
    extract_cgm_trend(data, result_df)
    extract_acceleration(data, result_df)
    extract_entropy(data, result_df)
    extract_fft(data, result_df)    

extract_features(mealDf.iloc[:,:-1], meal_features)
meal_features

# # PCA
pca = PCA(n_components=10)
#Fit meal features
principalComponents = pca.fit(meal_features)
#Transform meal features
PCA_mealdata = pca.fit_transform(meal_features)
PCA_mealdata

def CalcEucDist(a,b):
    return np.linalg.norm(a-b)

#KMeans clustering
kmeans = KMeans(n_clusters=nBins, random_state=0).fit(PCA_mealdata)

SSEKMeans = kmeans.inertia_


def calcEntropyPurity(labels):
    clusterBinMatrix = [[0 for i in range(nBins)] for i in range(nBins)]
    for i in range(labels.shape[0]):
        clusterBinMatrix[labels[i]][int(mealDf.iloc[i][30])] += 1
    Entropy = [0 for i in range(6)]
    Purity = 0
    totalPoints = sum(sum(clusterBinMatrix,[]))
    for i in range(len(clusterBinMatrix)):
        Purity += max(clusterBinMatrix[i])/totalPoints
        for j in range(len(clusterBinMatrix[i])):
            P = clusterBinMatrix[i][j]/sum(clusterBinMatrix[i])
            if(P != 0):
                Entropy[i] += (-P) * log2(P) * (sum(clusterBinMatrix[i])/totalPoints)    
    Entropy = sum(Entropy)
    return Entropy,Purity   

KmeansEntropy, KmeansPurity = calcEntropyPurity(kmeans.labels_)

#DBSCAN Clustering
db_default = DBSCAN(eps = 224, min_samples = 6).fit(PCA_mealdata) 
labels = db_default.labels_ 

for i in range(len(labels)):
    if labels[i] == -1:
        dist = float('inf')
        l = -1
        for j in range(len(labels)):
            if db_default.labels_[j] != -1:
                eucDist = CalcEucDist(PCA_mealdata[i], PCA_mealdata[j])
                if eucDist < dist:
                    dist = eucDist
                    l = db_default.labels_[j]
        labels[i] = l
db_default.labels_ = np.array(labels)

dbScanSSE = 0
for i in range(nBins):
    cluster = PCA_mealdata[db_default.labels_ == i]
    clusterMean = cluster.mean(axis = 0)
    dbScanSSE += ((cluster - clusterMean) ** 2).sum()

dbScanEntropy,dbScanPurity = calcEntropyPurity(db_default.labels_)


result = {
    'SSE for Kmeans': [SSEKMeans],
    'SSE for DBSCAN': [dbScanSSE],
    'Entropy for Kmeans': [KmeansEntropy],
    'Entropy for DBSCAN': [dbScanEntropy],
    'Purity for Kmeans': [KmeansPurity],
    'Purity for DBSCAN': [dbScanPurity]
}

resultDf = pd.DataFrame(result,index = [1])
resultDf.to_csv('Kumarasamy_Results.csv')
print("=====================Done===========================")

