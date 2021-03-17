import pandas as pd
import numpy as np



def config_param(stocks, sht, lng):
    
# CONFIGURANDO OS PARÂMETROS DA ESTRATÉGIA

    
    
    # Iniciando a tomada de decisão
    
    ## Se a média móvel de curto prazo for maior que a de longo prazo: Comprado (True)
    ## Se a média móvel de longo prazo for maior que a de curto prazo: Vendido (False)
    
    stocks['Status'] = stocks['Sht'] > stocks['Lng']
    
    # O start da decisão é a alteração do instante anterior (dia, hora, minuto). 
    # Se houver alteração de Status, está na hora da tomada da decisão.
    # Vamos usar o status do instante anterior ('.shift()'). Por padrão, '.shift()' utiliza 1 unidade como parâmetro.
    
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
