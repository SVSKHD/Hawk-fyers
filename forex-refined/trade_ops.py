import MetaTrader5 as mt5

class TradeOps:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError("MT5 Initialization failed")

    def place_trade(self, symbol, action='buy', lot=0.1, stop_loss=None, take_profit=None, magic=1001, comment="AutoTrade"):
        tick = mt5.symbol_info_tick(symbol)
        order_type = mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL
        price = tick.ask if action == 'buy' else tick.bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"Trade failed: {result.retcode}")
        return result

    def close_trade(self, ticket):
        pos = mt5.positions_get(ticket=ticket)[0]
        action_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(pos.symbol).bid if action_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": action_type,
            "position": ticket,
            "price": price,
            "magic": pos.magic,
            "comment": "Close by bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"Close failed: {result.retcode}")
        return result

    def modify_trade(self, ticket, new_sl=None, new_tp=None):
        pos = mt5.positions_get(ticket=ticket)[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": new_sl,
            "tp": new_tp
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"Modify failed: {result.retcode}")
        return result
