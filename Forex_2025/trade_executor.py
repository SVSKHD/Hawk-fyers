import MetaTrader5 as mt5

class TradeExecutor:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError("Failed to initialize MT5")

    def place_trade(self, symbol, direction, lot=0.5):
        action = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": action,
            "price": mt5.symbol_info_tick(symbol).ask if direction == "BUY" else mt5.symbol_info_tick(symbol).bid,
            "deviation": 10,
            "magic": 123456,
            "comment": f"{direction} trade by bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[ERROR] Trade failed for {symbol}: {result.retcode}")
        else:
            print(f"[TRADE] {direction} {symbol} @ {request['price']}, ticket: {result.order}")
        return result

    def close_trade(self, position_id, symbol):
        position = mt5.positions_get(ticket=position_id)
        if not position:
            print(f"[ERROR] Position {position_id} not found for {symbol}")
            return None

        direction = mt5.ORDER_TYPE_SELL if position[0].type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if direction == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position[0].volume,
            "type": direction,
            "position": position_id,
            "price": price,
            "deviation": 10,
            "magic": 123456,
            "comment": "Closing by bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[ERROR] Failed to close trade: {result.retcode}")
        else:
            print(f"[CLOSE] {symbol} @ {price}, ticket: {result.order}")
        return result

    def shutdown(self):
        mt5.shutdown()
