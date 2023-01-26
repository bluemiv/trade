# -*- coding: utf-8 -*-

import datetime

from upbit import core
from utils import config_parser
from utils import decoration


class Rsi:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['rsi']
        self._currency = self._options['trade_coin']
        self._init_krw = self._options['init_krw']
        self._buy_rsi = self._options['buy_rsi']
        self.log(f'Options: {self._options}')

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

    @decoration.forever(timer=10)
    def run(self):
        coin_account = self._upbit.get_balance(self._currency)
        current_price = self._upbit.get_current_price(self._currency)

        not_exists_account = coin_account is None
        if not_exists_account:
            # 매수
            rsi = self._upbit.get_min_rsi(self._currency)
            self.log(f'현재 rsi: {rsi}')
            if rsi <= self._buy_rsi:
                self.log(f'[매수] rsi {self._buy_rsi} 이하, {self._init_krw}원 매수 진행 (현재 가격: {current_price})')
                self._upbit.buy_market(self._currency, self._init_krw)
        else:
            # 매도 - 1% 이상일 전량 매도
            sell_rate = 1
            avg_coin_price = coin_account['avg_currency_price']
            rate = self._upbit.get_rate(current_price, avg_coin_price)
            if rate >= sell_rate:
                self.log(f'{sell_rate}% 이상, 이익 실현. 전량 매도 진행. rate: {rate} / balance: {coin_account["balance"]}')
                self._upbit.sell_market(self._currency, coin_account['balance'])
