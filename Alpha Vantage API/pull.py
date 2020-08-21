#!/usr/bin/python
# 
'''
sources 
https://www.youtube.com/watch?v=339AfkUQ67o
https://www.youtube.com/watch?v=JJO9fKj3_u4
https://www.youtube.com/watch?v=T2mQiesnx8s
https://www.youtube.com/watch?v=T2mQiesnx8s


Best practice
https://www.codementor.io/@satwikkansal/python-practices-for-efficient-code-performance-memory-and-usability-aze6oiq65
doc string https://www.youtube.com/watch?v=WOKxejxWJB4



'''

import pandas as pd
import numpy as np
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib.pyplot as plt
import sys
import random

#Variables
ticker = str(sys.argv[1])
mrkt = 'USD'


#multiple keys allow for higher rate of access to requests from free tier accounts
lines = open('keys').read().splitlines()
keys = random.choice(lines)

#pull data
time= CryptoCurrencies(key=keys, output_format = 'pandas')
data_ts , meta_data_ts = time.get_digital_currency_daily(symbol = ticker , market =mrkt )




#pulling closing values from time series 
#df_close = data_ts['4b. close (USD)']
df_close = pd.DataFrame(data_ts.iloc[:, 2])


#renaming column
df_close.columns = ['BTC_Daily_Close_USD']


#create 3 & 7 day rolling average
df_close['MA_3'] = df_close.BTC_Daily_Close_USD.rolling(3).mean()
df_close['MA_7'] = df_close.BTC_Daily_Close_USD.rolling(7).mean()







#drop the two last values so dataset starts on monday
df_test = df_close[['BTC_Daily_Close_USD']]
df_test =df_test[:-2]
#df_test['Date'] = df_test.index

#df_test['Date'] = pd.to_datetime(df_test['Date'])

#r = df_test.set_index('Date').groupby(pd.TimeGrouper('6M')).sum()
r = df_test.groupby(pd.Grouper(freq='W')).mean()
df_close['weekly_average'] = r

#print(ticker)
#print(df_close.columns)
print(df_close.tail())

#defining plot aesthetics
plt.rcParams.update({'font.size': 30})
figPres = plt.figure(figsize=(50,20))
axPres  = figPres.add_subplot(111)
axPres.yaxis.set_label_coords(-0.05,0.5)
axPres.xaxis.set_label_coords(0.5,-0.07)
#plt.grid(True)
#plt.legend(loc=2)
#creating a function to plot three plots








#1
plt.subplot(2,2,1)
plt.legend(  prop={'size': 30})
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
#plt.title('Value of Bitcoin over time', loc='center'  )



#3
#plt.title('3 & 7 Day Moving Average', loc='center'   )
plt.legend(  prop={'size': 30})
plt.ylabel('Value of Bitcoin (USD)')
plt.subplot(2,2,2)
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
plt.plot( df_close.index,df_close['MA_3'], label ='3 day MA')
plt.plot( df_close.index, df_close['MA_7'], label ='7 day MA' )


#4
#plt.title('Crypto Value + Weekly Averages', loc='center'  )
plt.legend(  prop={'size': 30})
plt.subplot(2,2,3)
plt.scatter( df_close.index,df_close['weekly_average'],  c='blue', label ='Weekly Averages')
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
plt.xlabel('Time')
plt.ylabel('Value of Bitcoin (USD)')



#1

#plt.title('Real Value, Moving Averages & Weekly Averages', loc='center'  )
plt.legend(  prop={'size': 30})
plt.subplot(2,2,4)
plt.scatter( df_close.index,df_close['weekly_average'],  c='blue', label ='Weekly Averages')
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
plt.plot( df_close.index,df_close['MA_3'], label ='3 day MA')
plt.plot( df_close.index, df_close['MA_7'], label ='7 day MA' )
plt.legend(  prop={'size': 30})
plt.xlabel('Time')

plt.suptitle('Bitcoin Time Seriece Analysis\nSource: Alpha Avantage API')
plt.savefig('Alpha_API_BTC_Analysis.png')

