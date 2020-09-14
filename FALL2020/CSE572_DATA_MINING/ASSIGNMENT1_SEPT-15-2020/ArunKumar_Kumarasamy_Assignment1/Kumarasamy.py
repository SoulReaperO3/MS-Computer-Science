import pandas
from math import log, pow

df = pandas.read_csv('../InsulinData.csv', parse_dates=[['Date','Time']],low_memory=False)
df = df[df["Alarm"].str.contains("AUTO MODE ACTIVE PLGM OFF")==True]        #AUTO MODE ACTIVE PLGM OFF
autoModeStartDate = df.loc[df.index[-1], "Date_Time"]

df = pandas.read_csv('../CGMData.csv', parse_dates=[['Date','Time']],low_memory=False)
autoModeDf = df.loc[df['Date_Time'] >= autoModeStartDate]
manualModeDf = df.loc[df['Date_Time'] < autoModeStartDate]
print('automode dataset:', autoModeDf.shape)
print('manualmode dataset:', manualModeDf.shape)

autoModeDateGrp = (autoModeDf['Date_Time'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Count'))
manualModeDateGrp = (manualModeDf['Date_Time'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Count'))

#autoModeDateGrp.to_csv('AutoModeDayCount.csv')
#manualModeDateGrp.to_csv('ManualModeDayCount.csv')  

errorRate = .1       #permissible error 10%
errorBound = .01     #error bound threshold value 1%

def findFromHoeffdingInequality(errorRate, errorBoundThreshold):
	return int((log(2/errorBoundThreshold))/(2*pow(errorRate,2)))

cgmPerDayThreshold = findFromHoeffdingInequality(errorRate, errorBound) 
print("cgmData Per Day Threshold: ", cgmPerDayThreshold) 

autoModeDateGrp = autoModeDateGrp[(autoModeDateGrp['Count'] >= cgmPerDayThreshold) & (autoModeDateGrp['Count'] <= 288)]
manualModeDateGrp = manualModeDateGrp[(manualModeDateGrp['Count'] >= cgmPerDayThreshold) & (manualModeDateGrp['Count'] <= 288)]

totalAutoModeDays = autoModeDateGrp.shape[0]
totalManualModeDays = manualModeDateGrp.shape[0]
#print(autoModeDateGrp)
print("Total Auto Mode Days: ", totalAutoModeDays)
print("Total Manual Mode Days: ", totalManualModeDays)

autoModeDf = autoModeDf[autoModeDf.Date_Time.dt.floor('d').isin(autoModeDateGrp['Date'])]
manualModeDf = manualModeDf[manualModeDf.Date_Time.dt.floor('d').isin(manualModeDateGrp['Date'])]

print("Manual Mode Data Frame:")
print(manualModeDf)

#autoModeDf.to_csv('autoModeDfCheck.csv') 
#manualModeDf.to_csv('ManualModeDFCheck.csv') 
wholeDayAutoPercentSum = [0] * 6
wholeDayManualPercentSum = [0] * 6
overNightAutoPercentSum = [0] * 6
overNightManualPercentSum = [0] * 6
dayTimeAutoPercentSum = [0] * 6
dayTimeManualPercentSum = [0] * 6

for date in autoModeDateGrp['Date']:
	perDayDf = autoModeDf.loc[autoModeDf['Date_Time'].dt.date == date.date()]
	wholeDayAutoPercentSum[0] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	wholeDayAutoPercentSum[1] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	wholeDayAutoPercentSum[2] += (perDayDf[(perDayDf['Sensor Glucose (mg/dL)']>=70) & (perDayDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	wholeDayAutoPercentSum[3] += (perDayDf[(perDayDf['Sensor Glucose (mg/dL)']>=70) & (perDayDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	wholeDayAutoPercentSum[4] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	wholeDayAutoPercentSum[5] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288

	overNightDf = autoModeDf.loc[(autoModeDf['Date_Time'].dt.date == date.date()) & (autoModeDf['Date_Time'].dt.time >= pandas.to_datetime('00:00:00').time()) & (autoModeDf['Date_Time'].dt.time < pandas.to_datetime('06:00:00').time())]
	overNightAutoPercentSum[0] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	overNightAutoPercentSum[1] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	overNightAutoPercentSum[2] += (overNightDf[(overNightDf['Sensor Glucose (mg/dL)']>=70) & (overNightDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	overNightAutoPercentSum[3] += (overNightDf[(overNightDf['Sensor Glucose (mg/dL)']>=70) & (overNightDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	overNightAutoPercentSum[4] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	overNightAutoPercentSum[5] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288	

	dayTimeDf = autoModeDf.loc[(autoModeDf['Date_Time'].dt.date == date.date()) & (autoModeDf['Date_Time'].dt.time >= pandas.to_datetime('06:00:00').time()) & (autoModeDf['Date_Time'].dt.time < pandas.to_datetime('11:59:59').time())]
	dayTimeAutoPercentSum[0] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	dayTimeAutoPercentSum[1] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	dayTimeAutoPercentSum[2] += (dayTimeDf[(dayTimeDf['Sensor Glucose (mg/dL)']>=70) & (dayTimeDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	dayTimeAutoPercentSum[3] += (dayTimeDf[(dayTimeDf['Sensor Glucose (mg/dL)']>=70) & (dayTimeDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	dayTimeAutoPercentSum[4] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	dayTimeAutoPercentSum[5] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288
	

for date in manualModeDateGrp['Date']:
	perDayDf = manualModeDf.loc[manualModeDf['Date_Time'].dt.date == date.date()]
	wholeDayManualPercentSum[0] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	wholeDayManualPercentSum[1] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	wholeDayManualPercentSum[2] += (perDayDf[(perDayDf['Sensor Glucose (mg/dL)']>=70) & (perDayDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	wholeDayManualPercentSum[3] += (perDayDf[(perDayDf['Sensor Glucose (mg/dL)']>=70) & (perDayDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	wholeDayManualPercentSum[4] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	wholeDayManualPercentSum[5] += (perDayDf[perDayDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288	

	overNightDf = manualModeDf.loc[(manualModeDf['Date_Time'].dt.date == date.date()) & (manualModeDf['Date_Time'].dt.time >= pandas.to_datetime('00:00:00').time()) & (manualModeDf['Date_Time'].dt.time < pandas.to_datetime('06:00:00').time())]
	overNightManualPercentSum[0] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	overNightManualPercentSum[1] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	overNightManualPercentSum[2] += (overNightDf[(overNightDf['Sensor Glucose (mg/dL)']>=70) & (overNightDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	overNightManualPercentSum[3] += (overNightDf[(overNightDf['Sensor Glucose (mg/dL)']>=70) & (overNightDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	overNightManualPercentSum[4] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	overNightManualPercentSum[5] += (overNightDf[overNightDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288	

	dayTimeDf = manualModeDf.loc[(manualModeDf['Date_Time'].dt.date == date.date()) & (manualModeDf['Date_Time'].dt.time >= pandas.to_datetime('06:00:00').time()) & (manualModeDf['Date_Time'].dt.time < pandas.to_datetime('11:59:59').time())]
	dayTimeManualPercentSum[0] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']>180].count()[1])*100/288
	dayTimeManualPercentSum[1] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']>250].count()[1])*100/288 
	dayTimeManualPercentSum[2] += (dayTimeDf[(dayTimeDf['Sensor Glucose (mg/dL)']>=70) & (dayTimeDf['Sensor Glucose (mg/dL)']<=180)].count()[1])*100/288
	dayTimeManualPercentSum[3] += (dayTimeDf[(dayTimeDf['Sensor Glucose (mg/dL)']>=70) & (dayTimeDf['Sensor Glucose (mg/dL)']<=150)].count()[1])*100/288
	dayTimeManualPercentSum[4] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']<70].count()[1])*100/288
	dayTimeManualPercentSum[5] += (dayTimeDf[dayTimeDf['Sensor Glucose (mg/dL)']<54].count()[1])*100/288
# 	# print(type(date))
data = {'Whole Day: Percentage time in hyperglycemia (CGM > 180 mg/dL)':[wholeDayManualPercentSum[0]/totalManualModeDays,wholeDayAutoPercentSum[0]/totalAutoModeDays],
		'Whole Day: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)':[wholeDayManualPercentSum[1]/totalManualModeDays,wholeDayAutoPercentSum[1]/totalAutoModeDays],
		'Whole Day: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)':[wholeDayManualPercentSum[2]/totalManualModeDays,wholeDayAutoPercentSum[2]/totalAutoModeDays],
		'Whole Day: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)':[wholeDayManualPercentSum[3]/totalManualModeDays,wholeDayAutoPercentSum[3]/totalAutoModeDays],
		'Whole Day: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)':[wholeDayManualPercentSum[4]/totalManualModeDays,wholeDayAutoPercentSum[4]/totalAutoModeDays],
		'Whole Day: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)':[wholeDayManualPercentSum[5]/totalManualModeDays,wholeDayAutoPercentSum[5]/totalAutoModeDays],
		
		'Overnight: Percentage time in hyperglycemia (CGM > 180 mg/dL)':[overNightManualPercentSum[0]/totalManualModeDays,overNightAutoPercentSum[0]/totalAutoModeDays],
		'Overnight: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)':[overNightManualPercentSum[1]/totalManualModeDays,overNightAutoPercentSum[1]/totalAutoModeDays],
		'Overnight: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)':[overNightManualPercentSum[2]/totalManualModeDays,overNightAutoPercentSum[2]/totalAutoModeDays],
		'Overnight: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)':[overNightManualPercentSum[3]/totalManualModeDays,overNightAutoPercentSum[3]/totalAutoModeDays],
		'Overnight: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)':[overNightManualPercentSum[4]/totalManualModeDays,overNightAutoPercentSum[4]/totalAutoModeDays],
		'Overnight: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)':[overNightManualPercentSum[5]/totalManualModeDays,overNightAutoPercentSum[5]/totalAutoModeDays],
		
		'Day Time: Percentage time in hyperglycemia (CGM > 180 mg/dL)':[dayTimeManualPercentSum[0]/totalManualModeDays,dayTimeAutoPercentSum[0]/totalAutoModeDays],
		'Day Time: percentage of time in hyperglycemia critical (CGM > 250 mg/dL)':[dayTimeManualPercentSum[1]/totalManualModeDays,dayTimeAutoPercentSum[1]/totalAutoModeDays],
		'Day Time: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)':[dayTimeManualPercentSum[2]/totalManualModeDays,dayTimeAutoPercentSum[2]/totalAutoModeDays],
		'Day Time: percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)':[dayTimeManualPercentSum[3]/totalManualModeDays,dayTimeAutoPercentSum[3]/totalAutoModeDays],
		'Day Time: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)':[dayTimeManualPercentSum[4]/totalManualModeDays,dayTimeAutoPercentSum[4]/totalAutoModeDays],
		'Day Time: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)':[dayTimeManualPercentSum[5]/totalManualModeDays,dayTimeAutoPercentSum[5]/totalAutoModeDays],
}


  
# # Creates pandas DataFrame. 
resultDf = pandas.DataFrame(data, index =['Manual Mode', 'Auto Mode']) 
resultDf.to_csv('Kumarasamy_Results.csv')