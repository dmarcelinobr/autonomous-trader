def buy(Ativo,lot):
    
    import MetaTrader5 as mt5
    
    mt5.initialize()
    symbol=Ativo
    mt5.symbol_select(symbol,True)

    lot=lot

    price= mt5.symbol_info_tick(symbol).ask

    deviation= 2

    request= {

        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': Ativo,
        'volume': float(lot),
        'type': mt5.ORDER_TYPE_BUY,
        'price': price,
        'sl': price - 200.00,
        'tp': price + 200.00,
        'deviation':deviation,
        'magic': 223456,
        'comment': 'Robo Gustavo',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN


    }

    result= mt5.order_send(request)

     

    mt5.shutdown()
    return result,price