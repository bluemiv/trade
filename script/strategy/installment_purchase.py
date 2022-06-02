# -*- coding: utf-8 -*-

'''
[분할매수/전량매도]
'''

import datetime
import time

from upbit.handler import UpbitHandler
from utils import config
from utils.deco import infinity_trade


class InstallmentPurchase:
    def __init__(self, init_krw=10000, sell_rate=3, buy_rate=-5):
        self._init_krw = init_krw

        self._sell_rate = sell_rate if sell_rate > 0 else sell_rate * -1
        self._buy_rate = buy_rate if buy_rate < 0 else buy_rate * -1

        _config = config.get_config()
        self._upbit = UpbitHandler(_config['access_key'], _config['secret_key'])

    def log(self, currency, message):
        now = datetime.datetime.now()
        print("{}\t{:<10}\t{}".format(now, currency, message))

    @infinity_trade(timer=10 * 60)
    def run(self):
        # 현재 자산 조회
        my_currency_list = self._upbit.valid_currency_filter(self._upbit.get_my_currency_list())
        delay = 10 / len(my_currency_list)

        for currency in my_currency_list:
            my_account_info = self._upbit.get_balance(currency)
            balance = my_account_info['balance']
            avg_currency_price = my_account_info['avg_currency_price']

            current_market_price = self._upbit.get_current_price(currency)
            rate = self._upbit.get_rate(current_market_price, avg_currency_price)

            self.log(currency, '{:f}%'.format(rate))

            # 3% 이상일때는 전량 매도
            if rate >= self._sell_rate:
                self.log(currency, '{}% 이상으로 이익 실현. 전량 매도 진행. rate: {} / balance: {}'.format(
                    self._sell_rate, rate, balance
                ))
                self._upbit.sell_market(currency, balance)

            # -5% 이하 일때는 추가 매수
            if rate <= self._buy_rate:
                self.log(currency, '{}% 이하로 손실중. 추가 매수 진행. rate: {}'.format(self._buy_rate, rate))
                self._upbit.buy_market(currency, self._init_krw)

            time.sleep(delay)
