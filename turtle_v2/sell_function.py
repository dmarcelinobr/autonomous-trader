def sell(Ativo,lot):
    
    import MetaTrader5 as mt5
    import pandas as pd
    
    mt5.initialize()
    symbol=Ativo
    mt5.symbol_select(symbol,True)

    lot=lot

    price= mt5.symbol_info_tick(symbol).bid

    deviation= 2

    request= {

        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': Ativo,
        'volume': float(lot),
        'type': mt5.ORDER_TYPE_SELL,
        'price': price,
        'sl': price + .20,
        'tp': price - .20,
        'deviation':deviation,
        'magic': 123456,
        'comment': 'Bot by Daniel Marcelino',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN


    }

    positions=mt5.positions_get(symbol=Ativo)
    positions=pd.DataFrame(positions)
    pos= positions[5].values
    valor=positions.values
    compra=pos[0]
    if valor.size<1:
        compra =0    
    
    if compra != 1:
        result= mt5.order_send(request)
    
    else:
        result=0

    mt5.shutdown()
    return result,price