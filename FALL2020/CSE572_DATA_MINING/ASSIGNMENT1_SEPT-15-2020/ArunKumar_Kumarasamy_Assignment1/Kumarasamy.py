import pandas

df = pandas.read_csv('../InsulinData.csv', parse_dates=[['Date','Time']],low_memory=False)
df = df[df["Alarm"].str.contains("AUTO MODE ACTIVE PLGM OFF")==True]        #AUTO MODE ACTIVE PLGM OFF
autoModeStartDate = df.loc[df.index[-1], "Date_Time"]
df = pandas.read_csv('../CGMData.csv', parse_dates=[['Date','Time']],low_memory=False)
autoModeDf = df.loc[df['Date_Time'] >= autoModeStartDate]
manualModeDf = df.loc[df['Date_Time'] < autoModeStartDate]
print('automode dataset:', autoModeDf.shape)
print('manualmode dataset:', manualModeDf.shape)

