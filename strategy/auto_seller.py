# -*- coding: utf-8 -*-

import datetime

from upbit import core
from utils import config_parser
from utils import decoration


class AutoSeller:
    def __init__(self):
        _config = config_parser.get_config()
        self._upbit = core.UpbitHandler(_config['access_key'], _config['secret_key'])
        self._options = _config['strategy']['auto_seller']
        self._currency = self._options['trade_coin']
        self._sell_rate = self._options['sell_rate']
        self.log(f'Options: {self._options}')

    def log(self, message):
        now = datetime.datetime.now()
        print("{:<20}\t{:<11}\t{}".format(str(now).split(".")[0], self._currency, message))

    @decoration.forever(timer=3)
    def run(self):
        coin_account = self._upbit.get_balance(self._currency)
        not_exists_account = coin_account is None
        if not_exists_account:
            self._upbit.cancel_all_order(self._currency)
            return

        # 매도
        current_price = self._upbit.get_current_price(self._currency)
        krw = coin_account['avg_krw_price']
        avg_coin_price = coin_account['avg_currency_price']
        rate = self._upbit.get_rate(current_price, avg_coin_price)
        self.log(f'현재 수익률: {rate}% / price: {krw}원 / balance: {coin_account["balance"]}')
        if rate >= self._sell_rate:
            self.log(
                f'{self._sell_rate}% 이상, 이익 실현. 전량 매도 진행. rate: {rate} / price: {krw}원 / balance: {coin_account["balance"]}')
            self._upbit.sell_market(self._currency, coin_account['balance'])
