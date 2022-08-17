# -*- coding: utf-8 -*-

import time

import pyupbit


class UpbitHandler:
    def __init__(self, access_key, secret_key):
        self._upbit = pyupbit.Upbit(access_key, secret_key)

        self._tickers = pyupbit.get_tickers()
        self._tickers.append('KRW')

        self._minium_price = int(5000 * 1.01)

    def _check_valid_currency(self, currency):
        """upbit에 상장된 올바른 currency인지 확인"""
        assert currency.upper() in self._tickers, "Invalid currency. currency: {}".format(currency)

    def _custom_balance_filter(self, info):
        """balance 정보를 사용하기 좋게 필터링"""
        if info['currency'] == 'KRW':
            krw = float(info['balance'])
            return {
                'currency': 'KRW',
                'balance': krw,
                'locked': float(info['locked']),
                'avg_currency_price': krw,
                'avg_krw_price': krw
            }
        currency = '{}-{}'.format(info['unit_currency'], info['currency']).upper()
        return {
            'currency': currency,
            'balance': float(info['balance']),
            'locked': float(info['locked']),
            'avg_currency_price': float(info['avg_buy_price']),
            'avg_krw_price': float(info['balance']) * float(info['avg_buy_price'])
        }

    def get_day_ma(self, currency, count=20):
        """이동평균선을 구한다

        Args:
            count: 이동평균선을 계산할 일 수
        """
        df = pyupbit.get_ohlcv(currency, count=count, interval='day')
        return df['close'].rolling(window=count, min_periods=1).mean().iloc[-1]

    def get_target_currency(self, rate=5):
        """트레이딩을 할 currency를 가져온다.
        이동평균선 근처에 있는 currency를 필터링"""
        _rate = rate if rate > 0 else rate * -1
        result = []

        for currency in self.get_tickers():
            ma = self.get_day_ma(currency)
            current_price = self.get_current_price(currency)
            rate = self.get_rate(current_price, ma)

            if rate >= -1 * _rate and rate <= _rate / 2:
                print("트레이드 대상 currency: {} / rate: {:f}%".format(currency, rate))
                result.append(currency)

            time.sleep(0.15)

        return result

    def get_tickers(self, without_krw=True, only_krw_market=True):
        """현재 upbit에 상장된 모든 currency 정보를 가지고 온다"""
        currency_list = self._tickers
        if without_krw:
            currency_list = list(filter(lambda x: x != 'KRW', currency_list))
        if only_krw_market:
            currency_list = list(filter(lambda x: x.startswith('KRW'), currency_list))
        return currency_list

    def valid_currency_filter(self, currency_list):
        """상장된 코인 또는 올바른 코인 currency만 필터링한다"""
        return list(filter(lambda x: x in self._tickers, currency_list))

    def get_balance(self, currency):
        """내가 가지고 있는 자산의 정보를 가지고 온다"""
        self._check_valid_currency(currency)
        all = self.get_balance_all()
        result = list(filter(lambda info: info['currency'] == currency.upper(), all))
        if len(result) > 0:
            return result[0]
        return None

    def get_balance_all(self):
        """내가 가지고 있는 전체 자산을 리스틀 형태로 가지고 온다"""
        result = []
        for info in self._upbit.get_balances():
            result.append(self._custom_balance_filter(info))
        return result

    def get_my_total_krw(self):
        """내 전체 자산을 조회한다"""
        return sum(
            list(map(lambda x: x['avg_krw_price'] + x['locked'] * x['avg_currency_price'], self.get_balance_all()))
        )

    def get_my_currency_list(self, without_krw=True, only_krw_market=True):
        """내가 가지고 있는 자산의 currency 목록을 조회한다"""
        currency_list = list(map(lambda x: x['currency'], self.get_balance_all()))
        if without_krw:
            currency_list = list(filter(lambda x: x != 'KRW', currency_list))
        if only_krw_market:
            currency_list = list(filter(lambda x: x.startswith('KRW'), currency_list))
        return currency_list

    def get_current_price(self, currency):
        """특정 currency의 현재 시장의 가격을 가지고 온다"""
        self._check_valid_currency(currency)
        return pyupbit.get_current_price(currency)

    def get_current_price_all(self, currency_list):
        """currency 리스트의 현재 시장의 가격을 가지고 온다

        Args:
            currency_list: 조회할 currency 목록
        """
        result = {}
        for currency in currency_list:
            _currency = currency.upper()
            result[_currency] = self.get_current_price(_currency)
        return result

    def buy_limit(self, currency, price, amount):
        """지정가로 매수한다

        Args:
            currency: 구매할 currency
            price: 지정가 매수 금액 (KRW 가 아닌 코인 금액)
            amount: 구매할 코인의 개수
        """
        self._check_valid_currency(currency)
        assert amount > 0, "Invalid amount. amount: {}".format(amount)
        assert price > 0, "Invalid price. price: {}".format(price)

        assert price * amount > self._minium_price, "Greater than {}WON. price: {}, amount: {}".format(
            self._minium_price, price, amount
        )

        # Response Data
        # {'uuid': '0a9e4c4f-83ed-442f-9390-1ef94f5f7f2a', 'side': 'bid', 'ord_type': 'limit', 'price': '10.0',
        #  'state': 'wait', 'market': 'KRW-XRP', 'created_at': '2022-06-02T18:28:44+09:00', 'volume': '1000.0',
        #  'remaining_volume': '1000.0', 'reserved_fee': '5.0', 'remaining_fee': '5.0', 'paid_fee': '0.0',
        #  'locked': '10005.0', 'executed_volume': '0.0', 'trades_count': 0}
        return self._upbit.buy_limit_order(currency, price, amount)

    def sell_limit(self, currency, price, amount):
        """지정가로 매도한다

        Args:
            currency: 매도할 currency
            price: 지정가 매도 금액 (KRW 가 아닌 코인 금액)
            amount: 매도할 코인의 개수
        """
        self._check_valid_currency(currency)
        assert amount > 0, "Invalid amount. amount: {}".format(amount)
        assert price > 0, "Invalid price. price: {}".format(price)

        assert price * amount > self._minium_price, "Greater than {}WON. price: {}, amount: {}".format(
            self._minium_price, price, amount
        )

        return self._upbit.sell_limit_order(currency, price, amount)

    def buy_market(self, currency, price):
        """시장가로 매수한다

        Args:
            currency: 매수할 currency
            price: 매수할 KRW 금액 (코인 금액이 아닌, KRW 금액)
        """
        _currency = currency.upper()
        self._check_valid_currency(_currency)
        assert price > self._minium_price, "Greater than {}WON. price: {}".format(self._minium_price, price)

        return self._upbit.buy_market_order(_currency, price)

    def sell_market(self, currency, amount):
        """시장가로 매도한다

        Args:
            currency: 매도할 currency
            amount: 매도할 KRW 금액 (코인 금액이 아닌, KRW 금액)
        """
        _currency = currency.upper()
        self._check_valid_currency(_currency)
        assert amount > 0, "Invalid amount. amount: {}".format(amount)

        return self._upbit.sell_market_order(_currency, amount)

    def get_rate(self, market, coin_price):
        """수익률을 가지고 온다

        Args:
            market: 현재 시장의 가격
            coin_price: 내 코인 가격
        """
        return (market - coin_price) / coin_price * 100
