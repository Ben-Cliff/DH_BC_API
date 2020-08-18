#!/usr/bin/python
# 
'''
sources 
https://www.youtube.com/watch?v=339AfkUQ67o
https://www.youtube.com/watch?v=JJO9fKj3_u4
https://www.youtube.com/watch?v=T2mQiesnx8s
https://www.youtube.com/watch?v=T2mQiesnx8s

'''

import pandas as pd
import numpy as np
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import sys
import random

#Variables
ticker = str(sys.argv[1])
mrkt = 'USD'
period = 7


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


#create 7 & 21 day rolling average
df_close['MA_7'] = df_close.BTC_Daily_Close_USD.rolling(7).mean()
df_close['MA_21'] = df_close.BTC_Daily_Close_USD.rolling(21).mean()


#plotting

plt.figure(figsize=(50,20))
plt.grid(True)
plt.plot(df_close['BTC_Daily_Close_USD'], label ='BTC')
plt.plot(df_close['MA_7'], label ='MA_7')
plt.plot(df_close['MA_21'], label ='MA_21')
plt.legend(loc=2)
plt.savefig('books_read.png')









print(ticker)
print(df_close.columns)
print(df_close)