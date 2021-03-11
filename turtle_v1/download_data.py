### Importando as bibliotecas.
import datetime as dt
import pandas as pd
import time
import numpy as np
from datetime import datetime
import warnings
import buy_function
import sell_function
warnings.filterwarnings('ignore')
import MetaTrader5 as mt5
# import pytz module for working with time zone
import pytz 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    
    
def download_data(Ativo,timeframe):
    
    
    from pytz import timezone
    A=datetime.now(timezone("America/Sao_Paulo"))
    NOW= A.hour
    dia=A.day
    mes= A.month
    ano= A.year
    # set time zone to UTC
    timezone = pytz.timezone("America/Sao_Paulo")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2020, 12, 10, tzinfo=timezone)
    utc_to = datetime(ano, mes, dia,NOW , tzinfo=timezone)
    # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
    rates = mt5.copy_rates_range(Ativo,timeframe, utc_from, utc_to)
     
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
     
    # create DataFrame out of the obtained data
    xfh = pd.DataFrame(rates)
    # convert time in seconds into the 'datetime' format
    xfh['time']=pd.to_datetime(xfh['time'], unit='s')
    xfh=xfh[['time', 'open', 'high', 'low', 'close','real_volume']]
    xfh.columns=['Date', 'Open', 'High', 'Low', 'Adj Close','Volume']
    xfh['Date'] = pd.to_datetime(xfh.Date)
    xfh.index = xfh.Date
    xfh.drop('Date', axis=1, inplace=True)
    xfh.dropna(inplace=True)
    #print(xfh.shape)
    #xfh.head(3)
    return xfh
