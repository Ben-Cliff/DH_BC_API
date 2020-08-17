#!/usr/bin/python
# 
'''
sources 
https://www.youtube.com/watch?v=339AfkUQ67o
https://www.youtube.com/watch?v=JJO9fKj3_u4

'''

import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import sys
import random

#read ticker argument
ticker = str(sys.argv[1])
mrkt = 'USD'


#multiple keys allow for higher rate of access to requests from free tier accounts
lines = open('keys').read().splitlines()
keys = random.choice(lines)

#pull data
time= CryptoCurrencies(key=keys, output_format = 'pandas')
data_ts, meta_data_ts = time.get_digital_currency_daily(symbol = ticker , market =mrkt )



period = 7 
#df1 = data_ts['4b. close (USD)'].iloc[period-1::]
#simple moving average// ie rolling average

ti = TechIndicators(key= keys ,output_format= 'pandas')
data_ti, meta_data_ti = ti.get_sma(symbol = 'BTC' , time_period=period,
                                    interval= 'daily', series_type= 'close')



#pulling closing values from time series 
df_closing = data_ts['4b. close (USD)']



print(ticker)
print(df_closing)