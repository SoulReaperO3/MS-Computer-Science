import pandas
from math import isclose

boolean = True
wholeDayPercentSum = [0] * 6
overNightPercentSum = [0] * 6
dayTimePercentSum = [0] * 6

df = pandas.read_csv('Kumarasamy_Results.csv')
for row in df.index:
	wholeDayPercentSum[0] = df.iloc[row]['Whole Day: Percentage time in hyperglycemia (CGM > 180 mg/dL)']
	wholeDayPercentSum[1] = df.iloc[row]['Whole Day: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)']
	wholeDayPercentSum[2] = df.iloc[row]['Whole Day: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)']
	wholeDayPercentSum[3] = df.iloc[row]['Whole Day: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)']
	wholeDayPercentSum[4] = df.iloc[row]['Whole Day: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)']
	wholeDayPercentSum[5] = df.iloc[row]['Whole Day: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)']

	overNightPercentSum[0] = df.iloc[row]['Overnight: Percentage time in hyperglycemia (CGM > 180 mg/dL)']
	overNightPercentSum[1] = df.iloc[row]['Overnight: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)']
	overNightPercentSum[2] = df.iloc[row]['Overnight: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)']
	overNightPercentSum[3] = df.iloc[row]['Overnight: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)']
	overNightPercentSum[4] = df.iloc[row]['Overnight: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)']
	overNightPercentSum[5] = df.iloc[row]['Overnight: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)']

	dayTimePercentSum[0] = df.iloc[row]['Day Time: Percentage time in hyperglycemia (CGM > 180 mg/dL)']
	dayTimePercentSum[1] = df.iloc[row]['Day Time: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)']
	dayTimePercentSum[2] = df.iloc[row]['Day Time: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)']
	dayTimePercentSum[3] = df.iloc[row]['Day Time: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)']
	dayTimePercentSum[4] = df.iloc[row]['Day Time: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)']
	dayTimePercentSum[5] = df.iloc[row]['Day Time: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)']

	for i in range(6):
		print(overNightPercentSum[i], " , ", dayTimePercentSum[i], " , ", overNightPercentSum[i] + dayTimePercentSum[i], " and ", wholeDayPercentSum[i])
		boolean = isclose((overNightPercentSum[i] + dayTimePercentSum[i]),wholeDayPercentSum[i], rel_tol=.1)
		if(boolean == False):
			break

if(boolean):
	print('Good to go')
else: 
	print('Error in code: overNight and daytime values do not add up to whole day value')
