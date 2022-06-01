# -*- coding: utf-8 -*-

'''
# 전략 1. 무한 매매
 - 10000원으로 구매
 - -10%일때 구매한 금액만큼 추가 매수
 - +5% 수익일때는 전량 매도
 - 15분 간격으로 배치 실행
'''

import utils.config as config_handler
import upbit.handler as upbit_handler


if __name__ == '__main__':
    config = config_handler.get_config()
    upbit = upbit_handler.UpbitHandler(config['access_key'], config['secret_key'])
    print(upbit.get_balance_all())
    # print(upbit.get_current_price('KRW-BTC'))
    # print(upbit.get_current_price_all(['KRW-BTC', 'KRW-XRP']))