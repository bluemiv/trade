# -*- coding: utf-8 -*-

import datetime
import math
import time

from upbit import core
from utils import config_parser
from utils import decoration

DEFAULT_OPTIONS = {
    'disabled_new_buy': False,
    'disabled_buy': False,
    'disabled_sell': False,
}


class Infinity:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['infinity']
        self._currency = self._options['trade_coin']
        self._init_krw = self._options['init_krw']
        self.log(f'Options: {self._options}')

        # self._buy_rate = buy_rate if buy_rate < 0 else buy_rate * -1
        # 
        # self._black_list = black_list if black_list is not None else []
        # 
        # self._options = DEFAULT_OPTIONS
        # if options is not None:
        #     for k, v in options.items():
        #         self._options[k] = v

    def _get_init_krw(self):
        """매수 금액을 설정한다"""
        min_krw, max_krw = (20000, 40000)
        result = int(self._upbit.get_my_total_krw() / 600)
        if result < min_krw:
            result = min_krw
        if result > max_krw:
            result = max_krw
        return int(result)

    def log(self, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], self._currency, message))

    def _get_price_delta(self, current_price):
        if 1 <= current_price < 10:
            return 0.01
        elif 10 <= current_price < 100:
            return 0.1
        elif 100 <= current_price < 1000:
            return 1
        elif 1000 <= current_price < 10000:
            return 5
        elif 10000 <= current_price < 100000:
            return 10
        elif 100000 <= current_price < 1000000:
            return 50

    @decoration.forever(timer=20 * 60)
    def run(self):
        # 모든 주문 취소
        self._upbit.cancel_all_order(self._currency)

        coin_account = self._upbit.get_balance(self._currency)

        current_price = self._upbit.get_current_price(self._currency)

        # 매수 예약
        not_exists_account = coin_account is None
        if not_exists_account:
            start_coin_price = current_price - self._get_price_delta(current_price) * 2
        else:
            avg_coin_price = coin_account['avg_currency_price']
            start_coin_price = math.floor(avg_coin_price) - self._get_price_delta(current_price) * 2

        self.log(f'[매수 예약 진행]')
        for idx in range(10):
            price = start_coin_price - idx
            self._upbit.buy_limit(self._currency, price, self._init_krw / price)
            self.log(f'>> [매수 예약] coin price: {price}')
            time.sleep(0.5)

        # 매도
        if not_exists_account:
            pass
        else:
            avg_coin_price = coin_account['avg_currency_price']

            # 1.5% 이상일 때 절반 매도
            sell_rate = 1.5
            rate = self._upbit.get_rate(current_price, avg_coin_price)
            if rate >= sell_rate:
                if coin_account['avg_krw_price'] <= self._init_krw:
                    # 전량 매도
                    half_balance = coin_account['balance'] / 2
                    self.log('{}% 이상으로 이익 실현. 전량 매도 진행. rate: {} / balance: {}'.format(
                        sell_rate, rate, half_balance
                    ))
                    self._upbit.sell_market(self._currency, half_balance)
                else:
                    # 절반 매도
                    self.log('{}% 이상으로 이익 실현. 절반 매도 진행. rate: {} / balance: {}'.format(
                        sell_rate, rate, coin_account['balance']
                    ))
                    self._upbit.sell_market(self._currency, coin_account['balance'])
