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
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"[ERROR] Failed to fetch tick data for {symbol}")
            return None

        price = tick.ask if direction == "BUY" else tick.bid

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
        if result is None:
            print(f"[CRITICAL] order_send returned None for {symbol} {direction}")
            return None
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(
                f"[ERROR] Trade failed for {symbol} {direction} | Retcode: {result.retcode} | Comment: {result.comment}")
        else:
            print(f"[SUCCESS] Trade placed: {symbol} {direction} | Ticket: {result.order}")
        return result

    def close_trade(self, ticket, symbol):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            print(f"[WARN] No position found with ticket {ticket} for {symbol}")
            return None

        pos_type = position[0].type
        volume = position[0].volume
        close_type = mt5.ORDER_TYPE_SELL if pos_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"[ERROR] Failed to fetch tick data for {symbol}")
            return None

        price = tick.bid if close_type == mt5.ORDER_TYPE_SELL else tick.ask

        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 10,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        result = mt5.order_send(close_request)
        if result is None:
            print(f"[CRITICAL] Close trade failed: order_send returned None for {symbol} ticket {ticket}")
            return None
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[ERROR] Close trade failed: {symbol} | Retcode: {result.retcode} | Comment: {result.comment}")
        else:
            print(f"[SUCCESS] Trade closed: {symbol} Ticket: {ticket}")
        return result
