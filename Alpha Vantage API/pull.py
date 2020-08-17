#!/usr/bin/python

import pandas
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import sys
import random

#read ticker argument
ticker = str(sys.argv[1])
mrkt = 'USD'


#multiple keys allow for higher rate of access to requests from free tier accounts
lines = open('keys').read().splitlines()
keys = random.choice(lines)

time= CryptoCurrencies(key=keys, output_format = 'pandas')
#data = time.get_intraday( symbol= ticker , interval = '1min', outputsize = 'full')
data = time.get_digital_currency_daily(symbol = ticker , market =mrkt )



print(ticker)
print(data) 