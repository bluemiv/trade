# -*- coding: utf-8 -*-

import math
import time
import logging

from upbit import core
from utils import config_parser


def init_logger():
    _logger = logging.getLogger()

    _logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    return _logger


if __name__ == "__main__":
    # init logger
    logger = init_logger()

    # load config
    config = config_parser.get_config()
    ACCESS_KEY = config["access_key"]
    SECRET_KEY = config["secret_key"]
    logger.info(f"access key: {ACCESS_KEY} / secret key: {SECRET_KEY}")

    upbit = core.UpbitHandler(ACCESS_KEY, SECRET_KEY)

    all_coin_list = upbit.get_krw_tickers()
    TARGET_COIN_LIST = list(filter(lambda x: x in all_coin_list, config["target_coin"]))
    logger.info(f"총 {len(TARGET_COIN_LIST)}개의 트레이드 대상 coin: {TARGET_COIN_LIST}")

    # 매수 금액 설정
    my_total_krw = upbit.get_my_total_krw()
    init_krw = math.floor(my_total_krw / 128)
    init_krw = 5000 * 1.01 if init_krw <= 5000 * 1.01 else init_krw
    init_krw = 30000 if init_krw >= 30000 else init_krw
    logger.info(f"현재 총 자산 {my_total_krw}원에 의해 설정된 매수 금액: {init_krw}")

    usable_krw = upbit.get_my_usable_krw()

    for currency in TARGET_COIN_LIST:
        logger.info(f"\n\n")
        logger.info(f"[TRADE START] currency: {currency}")

        coin_account = upbit.get_balance(currency)
        market_coin_price = upbit.get_current_price(currency)
        logger.info(f"> 현재 보유 중인 코인 정보: {coin_account}")
        logger.info(f"> 현재 코인의 시장 가격: {market_coin_price} {currency.replace('KRW-', '')}")

        can_buy = usable_krw > init_krw * 1.2

        # 매수를 한번도 안한 코인의 경우
        not_exists_account = coin_account is None
        if not_exists_account:
            rsi_minute = 10
            rsi = upbit.get_min_rsi(currency, rsi_minute)
            logger.info(f"> {rsi_minute}분 동안의 rsi: {rsi}")
            if rsi <= 45 and can_buy:
                logger.info(f"> rsi가 45 이하이므로, 첫 매수 {init_krw}원 진행")
                upbit.buy_market(currency, init_krw)

        # 매수를 한적이 있는 코인의 경우
        else:
            avg_coin_price = coin_account['avg_currency_price']
            rate = upbit.get_rate(market_coin_price, avg_coin_price)
            logger.info(f"> 현재 수익률: {rate}%")

            # 추가 매수
            if rate <= -5 and can_buy:
                logger.info(f"수익률 -5%이하로 추가 매수 {init_krw}원 진행")
                upbit.buy_market(currency, init_krw)

        time.sleep(0.25)
