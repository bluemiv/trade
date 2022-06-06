# -*- coding: utf-8 -*-

import datetime
import time

from upbit.handler import UpbitHandler
from utils import config
from utils.deco import infinity_trade


class InstallmentPurchase:
    def __init__(self, init_krw=None, sell_rate=3, buy_rate=-5, black_list=[]):
        _config = config.get_config()
        self._upbit = UpbitHandler(_config['access_key'], _config['secret_key'])

        self._init_krw = self._get_init_krw(init_krw)
        print("매수 금액:", self._init_krw)

        self._sell_rate = sell_rate if sell_rate > 0 else sell_rate * -1
        self._buy_rate = buy_rate if buy_rate < 0 else buy_rate * -1

        self._black_list = black_list

    def _get_init_krw(self, init_krw):
        """매수 금액을 설정한다"""
        min_krw = 10000
        max_krw = 50000
        if init_krw is None:
            result = int(self._upbit.get_my_total_krw() / 500)
            if result < min_krw:
                result = min_krw
            if result > max_krw:
                result = max_krw
        else:
            result = init_krw
        return int(result)

    def log(self, currency, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], currency, message))

    @infinity_trade(timer=8 * 60)
    def run(self):
        # 현재 자산 조회
        my_currency_list = self._upbit.valid_currency_filter(self._upbit.get_my_currency_list())
        target_currency_list = self._upbit.get_target_currency(rate=6)

        currency_list = []
        currency_list.extend(my_currency_list)
        currency_list.extend(target_currency_list)
        currency_list = list(set(currency_list))
        currency_list = list(filter(lambda x: x not in self._black_list, currency_list))

        delay = 10 / len(my_currency_list)

        for currency in currency_list:
            my_account_info = self._upbit.get_balance(currency)

            # 처음 매수
            if my_account_info is None:
                self.log(currency, '이평선 부근으로 매수 진행')
                self._upbit.buy_market(currency, self._init_krw)
                continue

            balance = my_account_info['balance']

            avg_currency_price = my_account_info['avg_currency_price']

            current_market_price = self._upbit.get_current_price(currency)
            rate = self._upbit.get_rate(current_market_price, avg_currency_price)

            self.log(currency, '{:f}%'.format(rate))

            # 일정 퍼센트 이상일때는 전량 매도
            if rate >= self._sell_rate:
                self.log(currency, '{}% 이상으로 이익 실현. 전량 매도 진행. rate: {} / balance: {}'.format(
                    self._sell_rate, rate, balance
                ))
                self._upbit.sell_market(currency, balance)

            # 일정 퍼센트 이하 일때는 추가 매수
            if rate <= self._buy_rate:
                self.log(currency, '{}% 이하로 손실중. 추가 매수 진행. rate: {}'.format(self._buy_rate, rate))
                self._upbit.buy_market(currency, self._init_krw)

            time.sleep(delay)
