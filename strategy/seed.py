# -*- coding: utf-8 -*-

import datetime
import time

from upbit import core
from utils import config_parser
from utils import decoration


class Seed:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['seed']

        self._black_list = self._options['black_list']

        self._min_krw = self._options['min_krw']
        self._max_krw = self._options['max_krw']

        self._buy_rate = self._options['buy_rate']
        self._buy_rate = self._buy_rate if self._buy_rate < 0 else -1 * self._buy_rate

        self._sell_rate = self._options['sell_rate']
        self._sell_rate = self._sell_rate if self._sell_rate > 0 else -1 * self._sell_rate

        self.log('', f'Options: {self._options}')

    def _get_init_krw(self):
        """매수 금액을 설정한다"""
        result = int(self._upbit.get_my_total_krw() / 15000000)
        if result < self._min_krw:
            result = self._min_krw
        if result > self._max_krw:
            result = self._max_krw
        return int(result)

    def log(self, currency, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], currency, message))

    def _get_target_currency_list(self):
        target_currency_list = self._upbit.get_target_currency(rate=10)
        raw_list = []
        raw_list.extend(target_currency_list)
        raw_list.extend(self._upbit.get_my_currency_list())
        raw_list = list(set(raw_list))
        my_currency_list = self._upbit.valid_currency_filter(raw_list)
        return list(filter(lambda x: x not in self._black_list, my_currency_list))

    @decoration.forever(timer=10)
    def run(self):
        init_krw = self._get_init_krw()
        self.log('', f"1회 매수 금액: {init_krw}")

        # 현재 자산 조회
        currency_list = self._get_target_currency_list()
        self.log('', f"자산: {currency_list}")

        for currency in currency_list:
            time.sleep(1)
            coin_account = self._upbit.get_balance(currency)

            # 없으면 매수
            not_exists_account = coin_account is None
            if not_exists_account:
                self.log(currency, f'신규 매수 진행. price: {init_krw}원')
                self._upbit.buy_market(currency, init_krw)
                continue

            # 있으면 추가 매수 또는 매도
            current_price = self._upbit.get_current_price(currency)

            krw = coin_account['avg_krw_price']
            balance = coin_account["balance"]

            avg_coin_price = coin_account['avg_currency_price']
            rate = self._upbit.get_rate(current_price, avg_coin_price)
            self.log(
                currency,
                f'현재 수익률: {rate}% / price: {krw}원 / balance: {balance}'
            )

            # 매도
            if rate >= self._sell_rate:
                self.log(
                    currency,
                    f'{self._sell_rate}% 이상, 이익 실현. 전량 매도 진행. rate: {rate} / price: {krw}원 / balance: {balance}'
                )
                self._upbit.sell_market(currency, coin_account['balance'])

            # 추가 매수
            if rate <= self._buy_rate:
                self.log(
                    currency,
                    f'{self._buy_rate}% 이하, 추가 매수 진행. rate: {rate} / price: {krw}원 / balance: {balance}'
                )
                self._upbit.buy_market(currency, init_krw)
