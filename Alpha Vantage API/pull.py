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

df_close.to_csv('BTC_Alpha.csv')



