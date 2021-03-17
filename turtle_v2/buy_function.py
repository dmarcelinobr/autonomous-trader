def buy(symbol, volume, sl = 0.0, tp = 0.0):    
    import MetaTrader5 as mt5
    import pandas as pd
    import numpy as np
    
    mt5.initialize()
    mt5.symbol_select(symbol,True)
    price = mt5.symbol_info_tick(symbol).ask
    
    deviation = 2
    magic_number = 987654321

    request= {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price + 1.00,
        "tp": price - 1.00,
        "deviation": deviation,
        "magic": magic_number,
        "comment": "Via Daniel's Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    positions = mt5.positions_get(symbol = symbol)
    positions = pd.DataFrame(positions)
    valor = positions.values
    
    
    if valor.size < 1:
        compra = 1
        
    if valor.size > 1:
        pos = positions[5].values
        compra = pos[0]   

    # send a trading request      
    if compra != 0:
        result = mt5.order_send(request)
    
    else:
        result = 0
     

    mt5.shutdown()
    return result,price