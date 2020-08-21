
import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies
#import sys
import random

#Variables
# ticker = str(sys.argv[1]) will extend functionality to take other crypto currency inputs 
ticker = 'BTC'
market = 'USD'
#Allow the use of multiple keys
lines = open('keys').read().splitlines()
keys = random.choice(lines)


#Define function to pull data
def alphaPull(keys,market, ticker):
    """
    This function takes in a valid Alpha Vantage API key, market symbol (eg. USD) 
    and Crypto commodity symbol (eg. BTC).
    It returns a time series database measuring daily closing values.
    Get a valid key here https://www.alphavantage.co/support/#api-key and paste it into ./keys
    """
    time= CryptoCurrencies(key=keys, output_format = 'pandas')
    data_ts , meta_data_ts = time.get_digital_currency_daily(symbol = ticker , market =market )

    #pulling closing values from time series 
    df_crypto_close = pd.DataFrame(data_ts.iloc[:, 2])
    #renaming column
    df_crypto_close.columns = ['BTC_Daily_Close_USD']
    return(df_crypto_close)



#df_close = alphaPull( 99 ,market, ticker )

try:
    df_close = alphaPull( keys ,market, ticker )
except Exception as e: 
    print('ERROR:\n')
    print(e)
    print('Note that the following key was used in this attempt:', keys )
    print('Please delete this above key from the keys folder and the follow the above link to get a new valid key.' )
    print('\n')


    #print('asdas')
    quit()

#Task
#Compute a 3-day and 7-day rolling average and report/visualise the results.

# create 3 & 7 day rolling average
df_close['MA_3'] = df_close.BTC_Daily_Close_USD.rolling(3).mean()
df_close['MA_7'] = df_close.BTC_Daily_Close_USD.rolling(7).mean()


#Task
#Compute the average price of each week (a week starts on a Monday and ends
#on Sunday) and report it

#drop the two last values so dataset starts on monday
df_temp = df_close[['BTC_Daily_Close_USD']]
df_temp =df_temp[:-2]

#Calculate weekly average
weekAvg = df_temp.groupby(pd.Grouper(freq='W')).mean()
df_close['weekly_average'] = weekAvg

#output dataset
df_close.to_csv('./Resources/BTC_Alpha.csv' ,index_label='date')

print('\n Success! See BTC_Alpha.csv file in the Resources directory. \nThe following key was used in this API call:', keys)
print('\n')