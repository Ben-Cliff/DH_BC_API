import pandas as pd
import matplotlib.pyplot as plt

try:
    df_close = pd.read_csv("./BTC_Alpha.csv")
except FileNotFoundError:
    print('ERROR: Please run $ python pull.py in the current directory to pull crypto currency data from Alpha Vantages API')
finally:
    quit()


###############PLOTTING#######################

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



#2
#plt.title('3 & 7 Day Moving Average', loc='center'   )
plt.legend(  prop={'size': 30})
plt.ylabel('Value of Bitcoin (USD)')
plt.subplot(2,2,2)
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
plt.plot( df_close.index,df_close['MA_3'], label ='3 day MA')
plt.plot( df_close.index, df_close['MA_7'], label ='7 day MA' )


#3
#plt.title('Crypto Value + Weekly Averages', loc='center'  )
plt.legend(  prop={'size': 30})
plt.subplot(2,2,3)
plt.scatter( df_close.index,df_close['weekly_average'],  c='blue', label ='Weekly Closing Averages')
plt.plot( df_close.index,df_close['BTC_Daily_Close_USD'], label ='BTC Value')
plt.xlabel('Time')
plt.ylabel('Value of Bitcoin (USD)')



#4
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




