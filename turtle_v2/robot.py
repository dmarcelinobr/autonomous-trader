### Importando as bibliotecas.
import datetime as dt
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
from buy_function import buy
from sell_function import sell

from download_data import download_data
from config_param import config_param
warnings.filterwarnings('ignore')
import MetaTrader5 as mt5
# import pytz module for working with time zone
import pytz 


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


RUN=1
while RUN==1:
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        mt5.shutdown() 

    # request connection status and parameters    
    info = mt5.terminal_info()
    if info.trade_allowed == False:
        print( "Auto-trading disabled in Terminal, enable it" )
        quit()

    #PARÂMETROS PARA O TRADING
    Ativo = 'PETR4'
    lotes = 1000
    
    #PARÂMETROS PARA AS MM
    sht = 5
    lng = 6
    
    timeframe = mt5.TIMEFRAME_M5
    
    xfh = download_data(Ativo, timeframe)
    stocks = xfh.copy()
    
    # Médias Móveis
    
    stocks['Sht'] = stocks['Adj Close'].rolling(window=sht).mean()
    stocks['Lng'] = stocks['Adj Close'].rolling(window=lng).mean()
    stocks.dropna(inplace=True)
    
    stocks = config_param(stocks, sht, lng)
    
    Var = stocks['action'].tail(1).values
    Var = Var[0]
    
    Var2 = stocks['Adj Close'].tail(1).values
    Var2 = Var2[0]
    
    Var3 = stocks['Sht'].tail(1).values
    Var3 = Var3[0]
    
    Var4 = stocks['Lng'].tail(1).values
    Var4 = Var4[0]
    
    if Var == 'buy':
       # check the execution result
       result,price = buy(symbol = Ativo, volume = lotes)
       print(result, style.BLUE)
       import time
       time.sleep(60)
    
    if Var == 'sell':
        # check the execution result
        result,price = sell(symbol = Ativo, volume = lotes)
        print(result, style.RED)
        import time
        time.sleep(60)

    print('')
    now = dt.datetime.now()
    # print(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(Var)
    print('Close: ${Var2:.2f} | Sht: ${Var3:.2f} | Lng: ${Var4:.2f}'.format(Var2=Var2, Var3=Var3, Var4=Var4),  style.RESET)
    # print(info.company)
    print('')
    import time
    time.sleep(60) # Sleep for 60 seconds