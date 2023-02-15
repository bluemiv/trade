# -*- coding: utf-8 -*-

import datetime
import time

from upbit import core
from utils import config_parser
from utils import decoration


class Rsi:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['rsi']
        self._black_list = self._options['black_list']
        self._init_krw = self._options['init_krw']
        self._buy_rsi = self._options['buy_rsi']

        self._add_buy_rate = self._options['add_buy_rate']
        self._add_buy_rate = self._add_buy_rate if self._add_buy_rate < 0 else self._add_buy_rate * -1

        self._sell_rate = self._options['sell_rate']
        self._sell_rate = self._sell_rate if self._sell_rate > 0 else self._sell_rate * -1

        self._ticker_count = self._options['ticker_count']

        self.log('', f'Options: {self._options}')

    def _get_init_krw(self):
        """매수 금액을 설정한다"""
        min_krw, max_krw = (20000, 40000)
        result = int(self._upbit.get_my_total_krw() / 600)
        if result < min_krw:
            result = min_krw
        if result > max_krw:
            result = max_krw
        return int(result)

    def log(self, currency, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], currency, message))

    @decoration.forever(timer=10)
    def run(self):
        for currency in self._upbit.get_tickers():
            if currency in self._black_list:
                continue
            time.sleep(0.25)

            coin_account = self._upbit.get_balance(currency)
            current_price = self._upbit.get_current_price(currency)
            not_exists_account = coin_account is None

            if not_exists_account:
                rsi = self._upbit.get_min_rsi(currency, self._ticker_count)
                if rsi <= self._buy_rsi:
                    # 매수
                    self.log(currency, f'[매수] rsi {self._buy_rsi} 이하, {self._init_krw}원 매수 진행 (현재 가격: {current_price})')
                    self._upbit.buy_market(currency, self._init_krw)

            else:
                avg_coin_price = coin_account['avg_currency_price']
                rate = self._upbit.get_rate(current_price, avg_coin_price)
                if rate <= self._add_buy_rate:
                    # 추가 매수
                    self.log(currency, f'{self._add_buy_rate}% 이하, {self._init_krw}원 추가 매수 진행. rate: {rate}')
                    self._upbit.buy_market(currency, self._init_krw)

                elif rate > self._sell_rate:
                    # 매도
                    krw = coin_account['avg_krw_price']
                    balance = coin_account["balance"]
                    self.log(
                        currency,
                        f'{self._sell_rate}% 이상, 이익 실현. 전량 매도 진행. rate: {rate} / price: {krw}원 / balance: {balance}'
                    )
                    self._upbit.sell_market(currency, coin_account['balance'])
