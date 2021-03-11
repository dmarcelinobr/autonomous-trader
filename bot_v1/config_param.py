import pandas as pd
import numpy as np

def config_param(stocks, sht, lng, Lenght):
    
# CONFIGURANDO OS PARÂMETROS DA ESTRATÉGIA

    ##-- Iniciando a tomada de decisão


    #1) usando médias móveis
    #stocks['Status'] = (stocks['Sht'] > stocks['Lng'])

    #2) usando macd
    #stocks['Status'] = (stocks['macd'] > stocks['macdsignal'])

    #3) usando SARTEXT
    #stocks['Status'] = (stocks['SAREXT'] > stocks['Adj Close'])

    #4) usando RSI
    #stocks['Status'] = stocks['RSISTATUS']
    #stocks = stocks[stocks['Status'] != 0]


    #b) -- Statusd-1 captura o Status do dia anterior.
    
    #stocks['Statusd-1'] = stocks['Status'].shift(1)

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    # Quando 'Status' e 'Statusd-1' forem diferentes, indica que a média móvel curta era                  #
    # menor que a longa em d-1 e ficou maior em d. Neste caso, has_action recebe como valor True.         #
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

    #stocks['has_action'] = stocks['Status'] != stocks['Statusd-1']

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    # #-Decisão da compra                                                                                #
    # Se a coluna 'has_action' for 'True', indica que houve mudança de Status entre d-1 e d. Se a coluna  #
    # 'Status' for 'True', indica que a média móvel curta está maior que a longa, ou seja, cruzou a longa #
    # de baixo para cima.                                                                                 #
    # Se 'RSI' <=40, mercado está sobrevendido, indica tendência de alta.                                 #
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

    #1) usando Médias Móveis como indicador de tendência
    #stocks.loc[(stocks['has_action']==True) &\
    #          (stocks['Status']==True) & (stocks['RSI'] <= 50), 'action'] = 'buy'

    #2) Sem RSI
    #stocks.loc[(stocks['has_action']==True) &\
    #          (stocks['Status']==True), 'action'] = 'buy'

    #2) usando CCI como indicador de tendência
    #stocks.loc[(stocks['has_action']==True) &\
    #              (stocks['Status']==True) & (stocks['CCISTATUS'] ==True), 'action'] = 'buy'
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    ##--Decisão da venda                                                                                     #
    # Se a coluna 'has_action' for 'True', indica que houve mudança de Status entre d-1 e d. Se a coluna   #
    # Status for 'False', indica que a média móvel curta está menor que a longa, ou seja, cruzou a longa   #
    # de cima para baixo.                                                                                  #
    # Se 'RSI' >= 60, mercado está sobrecomprado, indica tendência de queda.                               #
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    
    #1) usando RSI como indicador de tendência
    #stocks.loc[(stocks['has_action']==True) & (stocks['Status']==False) & (stocks['RSI'] >= 70) &\
    #          (stocks['Statusd-1'].notnull()), 'action'] = 'sell'

    #stocks.loc[(stocks['has_action']==True) & (stocks['Status']==False) &\
    #          (stocks['Statusd-1'].notnull()), 'action'] = 'sell'

    #2) usando CCI como indicador de tendência
    #stocks.loc[(stocks['has_action'] == True) & (stocks['Status'] == False) & (stocks['CCISTATUS'] ==True) & \
    #           (stocks['Statusd-1'].notnull()), 'action'] = 'sell'

    #c) Os registros que não forem 'buy' or 'sell', recebem o valor 'wait'.
    #stocks['action'].fillna('wait', inplace=True)


    ##--USANDO TOP/BOTTOM
    #j)--Estratégia Máximos e Mínimos

    stocks.loc[(stocks['Adj Close'] < stocks['MIN_' + str(Lenght)]), 'Status'] = True
    stocks.loc[(stocks['Adj Close'] > stocks['MAX_' + str(Lenght)]), 'Status'] = False
    stocks.Status.fillna('wait', inplace=True)
    #stocks = stocks[stocks['Status'] != 'wait']
    stocks['Statusd-1'] = stocks['Status'].shift(1)
    stocks['has_action'] = stocks['Status'] != stocks['Statusd-1']
    stocks.dropna(axis=0, inplace=True)

    ##-Racional
    stocks.loc[(stocks['has_action'] == True) & (stocks['Status'] == True), 'action'] = 'buy'
    stocks.loc[(stocks['has_action'] == True) & (stocks['Status'] == False), 'action'] = 'sell'
    stocks.action.fillna('wait', inplace=True)
    #print(stocks.action.tail(1).values)
    #print(stocks['Adj Close'].tail(1).values)
    return stocks
