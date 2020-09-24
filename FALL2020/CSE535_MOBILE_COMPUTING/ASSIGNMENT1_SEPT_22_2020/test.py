import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('D:\Studies\MS-Computer-Science\FALL2020\CSE535_MOBILE_COMPUTING\ASSIGNMENT1_SEPT_22_2020\CSVBreathe.csv',skiprows=450,nrows=450)
df2 = pd.read_csv('D:\Studies\MS-Computer-Science\FALL2020\CSE535_MOBILE_COMPUTING\ASSIGNMENT1_SEPT_22_2020\CSVBreathe2.csv')

list=df['0.0'].values.tolist()
list

i = 0
j = 20
for j in range(450):
    sum = 0.0
    k = i
    for k in range(j):
            sum += list[k]
    list[i] = sum / 20;
    i += 1

list
df2 = pd.DataFrame(list)


plt.plot(df)
plt.plot(df2,color = 'orange')
plt.show()

