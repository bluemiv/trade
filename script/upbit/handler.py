# -*- coding: utf-8 -*-

import pyupbit

class UpbitHandler:
    def __init__(self, access_key, secret_key):
        self._upbit = pyupbit.Upbit(access_key, secret_key)

        self._tickers = pyupbit.get_tickers()
        self._tickers.append('KRW')

    def _check_symbol(self, symbol):
        assert symbol.upper() in self._tickers, "Invalid symbol. symbol: {}".format(symbol)

    def get_balance(self, symbol):
        """내가 가지고 있는 자산의 balance를 가지고 온다"""
        self._check_symbol(symbol)
        return self._upbit.get_balance(symbol.upper())

    def get_balance_all(self):
        """내가 가지고 있는 전체 자산을 dictionary로 가지고 온다"""
        result = {}
        for info in self._upbit.get_balances():
            if info['currency'] == 'KRW':
                krw = float(info['balance'])
                result['KRW'] = {
                    'balance': krw,
                    'locked': float(info['locked']),
                    'avg_symbol_price': krw,
                    'avg_krw_price': krw
                }
            else:
                symbol = '{}-{}'.format(info['unit_currency'], info['currency']).upper()
                result[symbol] = {
                    'balance': float(info['balance']),
                    'locked': float(info['locked']),
                    'avg_symbol_price': float(info['avg_buy_price']),
                    'avg_krw_price': float(info['balance']) * float(info['avg_buy_price'])
                }
        return result

    def get_current_price(self, symbol):
        """특정 symbol의 현재 시장의 가격을 가지고 온다"""
        self._check_symbol(symbol)
        return pyupbit.get_current_price(symbol)

    def get_current_price_all(self, symbol_list):
        """symbol 리스트의 현재 시장의 가격을 가지고 온다

        Args:
            symbol_list: 조회할 symbol 목록
        """
        result = {}
        for symbol in symbol_list:
            _symbol = symbol.upper()
            result[_symbol] = self.get_current_price(_symbol)
        return result