#!/usr/bin/python

import pandas
from alpha_vantage.timeseries import TimeSeries
import sys
import random

#read ticker argument
ticker = str(sys.argv[1])
#mrkt = 'USD'


#multiple keys allow for higher rate of access to requests from free tier accounts
lines = open('keys').read().splitlines()
keys = random.choice(lines)

time= TimeSeries(key=keys, output_format = 'pandas')
data = time.get_intraday( symbol= ticker , interval = '1min', outputsize = 'full')
#data = get_digital_currency_daily 



print(ticker)
print(data) 