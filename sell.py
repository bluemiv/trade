# -*- coding: utf-8 -*-

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

    for currency in TARGET_COIN_LIST:
        logger.info(f"\n\n")
        logger.info(f"[TRADE START] currency: {currency}")

        coin_account = upbit.get_balance(currency)

        # 매수를 한번도 안한 코인의 경우, skip
        not_exists_account = coin_account is None
        if not_exists_account:
            continue

        market_coin_price = upbit.get_current_price(currency)
        logger.info(f"> 현재 보유 중인 코인 정보: {coin_account}")
        logger.info(f"> 현재 코인의 시장 가격: {market_coin_price} {currency.replace('KRW-', '')}")

        avg_coin_price = coin_account['avg_currency_price']
        rate = upbit.get_rate(market_coin_price, avg_coin_price)
        logger.info(f"> 현재 수익률: {rate}%")

        # 매도
        if rate >= 1.5:
            logger.info(f"수익률 1.5%이상으로 전량 매도. {coin_account['avg_krw_price']}원 이익 실현.")
            upbit.sell_market(currency, coin_account['balance'])

        time.sleep(0.25)
