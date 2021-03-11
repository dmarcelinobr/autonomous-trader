# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:14:11 2021

@author: daniel
"""

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


def config_param(stocks,sht,lng):
    
# CONFIGURANDO OS PARÂMETROS DA ESTRATÉGIA

    
    
    # Iniciando a tomada de decisão
    
    ## Se a média móvel de curto prazo for maior que a de longo prazo: Comprado (True)
    ## Se a média móvel de longo prazo for maior que a de curto prazo: Vendido (False)
    
    stocks['Status'] = stocks['Sht'] > stocks['Lng']
    
    ## O start da decisão é a alteração do dia anterior. Se houver alteração de Status, está na hora da tomada da decisão.
    ## Vamos usar o status do dia anterior ('.shift()'). Por padrão, '.shift()' utiliza 1 dia como parâmetro.
    
    stocks['Statusd-1'] = stocks['Status'].shift(1)
    
    ## Vamos criar agora a coluna que aciona a estratégia.
    ## has-action é true quando o Status de D é diferente de D-1.
    
    stocks['has_action'] = stocks['Status'] != stocks['Statusd-1']

    ### Decisão da compra
    
    stocks.loc[(stocks['has_action']==True) &\
              (stocks['Status']==True), 'action'] = 'buy'
    
    
    # Decisão de venda
    
    # Vamos criar agora a condição de venda do ativo, quando has_action for True e Status for False e
    # Statusd-1 não for valor nulo, pois não tem como vender o que não foi comprado ainda.
    
    stocks.loc[(stocks['has_action']==True) & (stocks['Status']==False) &\
              (stocks['Statusd-1'].notnull()), 'action'] = 'sell'
    
    stocks['action'].fillna('wait', inplace=True)
    return stocks



def download_data(Ativo,timeframe):
    
    
    from pytz import timezone
    A = datetime.now(timezone("America/Sao_Paulo"))
    NOW = A.hour
    dia = A.day
    mes = A.month
    ano = A.year
    # set time zone to UTC
    timezone = pytz.timezone("America/Sao_Paulo")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2021, 1, 1, tzinfo=timezone)
    utc_to = datetime(ano, mes, dia,NOW , tzinfo=timezone)
    # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
    rates = mt5.copy_rates_range(Ativo,timeframe, utc_from, utc_to)
     
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
     
    # create DataFrame out of the obtained data
    xfh = pd.DataFrame(rates)
    # convert time in seconds into the 'datetime' format
    xfh['time']=pd.to_datetime(xfh['time'], unit='s')
    
    
    
    print(xfh.shape)
    xfh=xfh[['time','close','real_volume']]
    xfh.columns=['Date','Adj Close','Volume']
    xfh['Date'] = pd.to_datetime(xfh.Date)
    xfh.index = xfh.Date
    xfh.drop('Date', axis=1, inplace=True)
    xfh.dropna(inplace=True)
    print(xfh.shape)
    return xfh




def sell(Ativo,lot):
    import MetaTrader5 as mt5
    import pandas as pd
    
    mt5.initialize()
    symbol=Ativo
    mt5.symbol_select(symbol,True)

    lot = lot

    price = mt5.symbol_info_tick(symbol).bid

    deviation = 2

    request= {

        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': Ativo,
        'volume': float(lot),
        'type': mt5.ORDER_TYPE_SELL,
        'price': price,
        'sl': price + 1.00,
        'tp': price - 1.00,
        'deviation':deviation,
        'magic': 123456,
        'comment': 'Bot by Daniel Marcelino',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN


    }

    positions = mt5.positions_get(symbol=Ativo)
    positions = pd.DataFrame(positions)
    print(positions)
    pos = positions[5].values
    if pos[0] != 1:
        result= mt5.order_send(request)
    
    else:
        result=0

    mt5.shutdown()
    return result,price



if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
        
    
Ativo = 'PETR4'
lot = 100
    
#PARÂMETROS PARA AS MM
sht = 5
lng = 6
    
timeframe = mt5.TIMEFRAME_M5
    
xfh = download_data(Ativo,timeframe)
stocks = xfh.copy()
    
    # Médias Móveis
    
stocks['Sht'] = stocks['Adj Close'].rolling(window=sht).mean()
stocks['Lng'] = stocks['Adj Close'].rolling(window=lng).mean()
stocks.dropna(inplace=True)
    
stocks = config_param(stocks,sht,lng)
    
Var = stocks['action'].tail(1).values
Var = Var[0]
    
Var2 = stocks['Adj Close'].tail(1).values
Var2 = Var2[0]
    
Var3 = stocks['Sht'].tail(1).values
Var3 = Var3[0]
    
Var4 = stocks['Lng'].tail(1).values
Var4 = Var4[0]
    
print(stocks)


result,price = buy(Ativo,lot)
print(result)
    
result,price = sell(Ativo,lot)
print(result)
        