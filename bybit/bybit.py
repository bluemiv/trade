# -*- coding: utf-8 -*-

from pybit import HTTP


class ByBit():

    def __init__(self, api_key, secret_key, spot=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = HTTP(
            endpoint="https://api.bybit.com",
            api_key=self.api_key,
            api_secret=self.secret_key,
            spot=spot
        )

    def get_target_symbol(self, symbol):
        symbols = self.session.query_symbol()
        result = symbols['result']
        return list(filter(lambda x: x["name"] == symbol, result))

    def get_my_account(self, symbol):
        return self.session.get_wallet_balance(symbol=symbol)["result"]

    def get_my_position(self, symbol):
        return self.session.my_position(symbol=symbol)["result"]

    def get_order_book(self, symbol):
        return self.session.orderbook(symbol=symbol)["result"]

    def set_leverage(self, symbol, leverage):
        self.session.set_leverage(
            symbol=symbol,
            leverage=leverage,
            leverage_only=True
        )

    def open_short(self, symbol, qty, price):
        return self.session.place_active_order(
            symbol=symbol,
            side="Sell",
            order_type="Limit",
            qty=qty,
            price=price,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False
        )

    def close_short(self, symbol, qty, price):
        return self.session.place_active_order(
            symbol=symbol,
            side="Buy",
            order_type="Limit",
            qty=qty,
            price=price,
            time_in_force="GoodTillCancel",
            reduce_only=True,
            close_on_trigger=False
        )

    def close_long(self, symbol, qty, price):
        return self.session.place_active_order(
            symbol=symbol,
            side="Sell",
            order_type="Limit",
            qty=qty,
            price=price,
            time_in_force="GoodTillCancel",
            reduce_only=True,
            close_on_trigger=False
        )

    def query_active_order(self, symbol):
        return self.session.query_active_order(symbol=symbol)["result"]

    def cancel_active_order(self, symbol, order_id):
        return self.session.cancel_active_order(symbol=symbol, order_id=order_id)

    def full_partial_position_tp_sl_switch(self, symbol):
        return self.session.full_partial_position_tp_sl_switch(symbol=symbol)
