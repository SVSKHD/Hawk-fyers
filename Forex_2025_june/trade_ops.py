# trade_ops.py
import MetaTrader5 as mt5

class TradeExecutor:
    def __init__(self):
        if not mt5.initialize():
            raise Exception("MT5 initialization failed")

    def shutdown(self):
        mt5.shutdown()

    def place_trade(self, symbol, direction, lot=0.5):
        order_type = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).ask if direction == "BUY" else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        result = mt5.order_send(request)
        return result

    def close_trade(self, ticket, symbol):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return None
        pos_type = position[0].type
        close_type = mt5.ORDER_TYPE_SELL if pos_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if close_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position[0].volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 10,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        result = mt5.order_send(close_request)
        return result
