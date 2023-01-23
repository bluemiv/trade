# -*- coding: utf-8 -*-

import datetime
import math
import time

from upbit import core
from utils import config_parser
from utils import decoration


class Infinity:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['infinity']
        self._currency = self._options['trade_coin']
        self._init_krw = self._options['init_krw']
        self.log(f'Options: {self._options}')

    def log(self, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], self._currency, message))

    @decoration.forever(timer=10 * 60)
    def run(self):
        # 모든 주문 취소
        self._upbit.cancel_all_order(self._currency)

        coin_account = self._upbit.get_balance(self._currency)

        current_price = self._upbit.get_current_price(self._currency)

        # 매수 예약
        exists_account = coin_account is not None
        delta_price = self._upbit.get_price_delta(current_price)
        start_coin_price = current_price - delta_price * 2
        if exists_account:
            avg_coin_price = coin_account['avg_currency_price']
            start_coin_price_from_account = math.floor(avg_coin_price) - delta_price * 2
            start_coin_price = min(start_coin_price, start_coin_price_from_account)

        self.log(f'[매수 예약 진행]')
        for idx in range(7):
            price = round(start_coin_price - idx * delta_price, 4)
            self._upbit.buy_limit(self._currency, price, self._init_krw / price)
            self.log(f'>> [매수 예약] coin price: {price}')
            time.sleep(0.25)

        # 매도
        if exists_account:
            avg_coin_price = coin_account['avg_currency_price']

            # 1.5% 이상일 매도
            sell_rate = 1.5
            rate = self._upbit.get_rate(current_price, avg_coin_price)
            self.log(f'>> 현재 수익: {rate}%')
            if rate >= sell_rate:
                if coin_account['avg_krw_price'] / 2 <= self._init_krw:
                    # 전량 매도
                    self.log('{}% 이상으로 이익 실현. 전량 매도 진행. rate: {} / balance: {}'.format(
                        sell_rate, rate, coin_account['balance']
                    ))
                    self._upbit.sell_market(self._currency, coin_account['balance'])

                else:
                    # 절반 매도
                    half_balance = coin_account['balance'] / 2
                    self.log('{}% 이상으로 이익 실현. 절반 매도 진행. rate: {} / balance: {}'.format(
                        sell_rate, rate, half_balance
                    ))
                    self._upbit.sell_market(self._currency, half_balance)
