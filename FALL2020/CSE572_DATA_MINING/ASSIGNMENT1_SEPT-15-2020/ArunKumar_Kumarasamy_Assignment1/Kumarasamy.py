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

#print(autoModeDateGrp)

autoModeDf = autoModeDf[autoModeDf.Date_Time.dt.floor('d').isin(autoModeDateGrp['Date'])]
manualModeDf = manualModeDf[manualModeDf.Date_Time.dt.floor('d').isin(manualModeDateGrp['Date'])]

print("Manual Mode Data Frame:")
print(manualModeDf)

#autoModeDf.to_csv('autoModeDfCheck.csv') 
#manualModeDf.to_csv('ManualModeDFCheck.csv') 
