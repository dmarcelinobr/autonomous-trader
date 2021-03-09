### Importando as bibliotecas.

import pandas as pd                     ## manipulação de dataframes em python
import time                             ## manipulação de tempo
import numpy as np                      ## manipulação de arrays e vetores
import talib as ta                      ## criação de indicadores técnicos
from datetime import datetime           ## manipulação de datas em pyton
import datetime as dt                   ## manipulação de datas em python
from buy_function import buy            ## função de compra de ativos
from sell_function import sell          ## função de vendas de ativos
from download_data import download_data ## função para download dos dados em tempo real
from config_param import config_param   ## função de configuração da estratégia de compra/venda
import warnings                         ## filtros para avisos
warnings.filterwarnings('ignore')       ## ignorar aviso
import MetaTrader5 as mt5               ## biblioteca do MT5 para Python
import pytz                             ## manipulação de time zones em python


##A) Iniciando uma sessão do MT5 com um looping

RUN=1
while RUN==1:

    # Estabelecendo uma conexão com o Terminal do MetaTrader5
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
        
    ## Definindo o ativo usado no robô
    Ativo='CCMH21'

    ## Ajustando a quantidade de lotes que serão comprados/vendidos
    lot= 1

    ## Ajustando o timeframe (M1 para 1 minuto / M5 para 5 minutos / D1 para diário
    timeframe = mt5.TIMEFRAME_D


    ## Carregando as cotações em tempo real através da função download_data
    xfh = download_data(Ativo,timeframe)    ## Parâmetros: Ativo e o timeframe configurado

    #Criando um novo objeto que recebe o dataframe com os dados em tempo real
    stocks = xfh.copy()

    # PARTE IV - CRIANDO A ESTRATÉGIA

    #ETAPA II) Suavização da Série

    # a) Suavização da série

    suavização = 5

    # b) Gerando as features OHLC suavizadas

    stocks['EMAC'] = ta.EMA(stocks['Adj Close'], timeperiod=suavização)  # Suavização da série de fechamento
    stocks['EMAO'] = ta.EMA(stocks['Open'], timeperiod=suavização)  # Suavização da série de abertura
    stocks['EMAH'] = ta.EMA(stocks['High'], timeperiod=suavização)  # Suavização da série de Altas
    stocks['EMAL'] = ta.EMA(stocks['Low'], timeperiod=suavização)  # Suavização da série de Baixas
    stocks['EMAV'] = ta.EMA(stocks['Volume'], timeperiod=suavização)  # Suavização da série de Volume

    #ETAPA III)

    ##-- Gerando os Osciladores e Indicadores de Tendência

    # 1) RSI - Relative Strength Index
    stocks['RSI'] = ta.RSI(stocks['EMAC'], timeperiod=14)
    # 2) MACD - Moving Average Convergence/Divergence
    stocks['macd'], stocks['macdsignal'], stocks['macdhist'] = ta.MACD(stocks['EMAC'], fastperiod=12, slowperiod=26, signalperiod=9)
    # 3) Parabolic SAR
    stocks['SAR'] = ta.SAR(stocks['EMAH'], stocks['EMAL'], 0.02, 0.3)
    stocks['SAREXT'] = ta.SAREXT(stocks['EMAH'], stocks['EMAL'], 0.02, 0.3)
    # 4) CCI - Commodity Channel Index
    stocks['CCI'] = ta.CCI(stocks['EMAH'], stocks['EMAL'], stocks['EMAC'], timeperiod=14)
    # 5) SMA - Single Moving Average
    sht = 5
    lng = 22
    stocks['SHT'] = stocks['Adj Close'].rolling(window=sht).mean()
    stocks['LNG'] = stocks['Adj Close'].rolling(window=lng).mean()
    # 6) Bollinger Bands
    stocks['UPP'], stocks['MIDD'], stocks['LOW'] = ta.BBANDS(stocks['EMAC'], timeperiod=6, nbdevup=4, nbdevdn=4, matype=0)
    # 7) Top & Bottom
    stocks['Close20d'] = stocks['Adj Close'].shift(20)
    stocks['Close30d'] = stocks['Adj Close'].shift(30)
    stocks['Close40d'] = stocks['Adj Close'].shift(40)
    stocks['Close50d'] = stocks['Adj Close'].shift(50)
    stocks['Close60d'] = stocks['Adj Close'].shift(60)
    # 8) TOP & BOTTOM
    Lenght = 60
    stocks['MIN_' + str(Lenght)] = list(np.zeros(len(stocks)))
    stocks['MAX_' + str(Lenght)] = list(np.zeros(len(stocks)))
    for i in range(len(stocks) - Lenght):
        stocks['MIN_' + str(Lenght)][i + Lenght] = stocks['Adj Close'][i:i + Lenght].min()
        stocks['MAX_' + str(Lenght)][i + Lenght] = stocks['Adj Close'][i:i + Lenght].max()
    stocks.dropna(axis=0, inplace=True)

    #===================================================================================================================
    # A ESTRATÉGIA DE COMPRA/VENDA DEVE SER INSERIDA NO BLOCO ABAIXO
    #===================================================================================================================

    stocks['Status'] = stocks['SHT'] > stocks['LNG']

    # ==================================================================================================================
    # ==================================================================================================================


    # Executando a função 'config_param' e passando a série

    stocks=config_param(stocks, sht, lng, Lenght)

    ## Criando variáveis com os últimos resultados os indicadores estratégicos

    Var= stocks['action'].tail(1).values
    Var=Var[0]
    #Var7 = stocks['has_action'].tail(1).values
    #Var7 = Var7[0]
    Var1 = stocks['Adj Close'].tail(1).values
    Var1 = Var1[0]
    Var2 = stocks['MIN_' + str(Lenght)].tail(1).values
    Var2 = Var2[0]
    Var3 = stocks['MAX_' + str(Lenght)].tail(1).values
    Var3 = Var3[0]
    #Var4 = stocks['UPP'].tail(1).values
    #Var4 = Var4[0]
    #Var5 = stocks['LOW'].tail(1).values
    #Var5 = Var5[0]


    #Ordens de Compra
    if Var=='buy':
        
        result,price= buy(Ativo,lot)
        #print(result)
        import time
        time.sleep(60)

    #Ordens de Venda
    if Var=='sell':
        
        result,price= sell(Ativo,lot)
        #print(result)
        import time
        time.sleep(60)

    #Imprimindo os valores de cada indicador


    if Var1 < Var2:
        print(f'Entry Point - Buy //// Price {Var1:.0f}')
        print(f'Price {Var1:.0f} < {Var2:.0f} (Mínimo {Lenght} dias)')
    elif Var1 > Var3:
        print(f'Entry Point - Sell //// Price {Var3:.2f}')
        print(f'Price {Var1:.0f} > {Var3:.0f} (Máximo {Lenght} dias)')
    else:
        print('No Entry Point --- :(   ')
        print(f'Mínimo - {Var2:.0f} < Price {Var1:.0f} < Máximo {Var3:.0f}')


    '''
    if Var1 > Var4:
        print('Price: ', Var1, '>', 'UPP: ', Var4, ' & ', 'CCI > 100 ', Var5)
    elif Var1 < Var5:
        print('Price: ', Var1, '<', 'LOW: ', Var4, ' & ', 'CCI < -100 ', Var5)
    else:
        print('No entry point {::} :(')
    '''
    #import time

    #time.sleep(60) # Sleep for 1 seconds



