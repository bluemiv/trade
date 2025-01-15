# -*- coding: utf-8 -*-
import time

from pybit.unified_trading import HTTP

from core.bybit_helper import BybitHelper
from utils.config import get_config


def main():
    bybit_config = get_config()["bybit"]
    helper = BybitHelper(config=bybit_config)

    for symbol in helper.get_target_symbols():
        print(f"-*-*- {symbol} 매매 시작 -*-*-")

        helper.cancel_all_orders(symbol)

        qty, next_qty = helper.get_entry_qty(symbol)
        print(f" >> [DEBUG] 첫 진입 개수: {qty}, 추가 진입 개수: {next_qty}")

        position = helper.get_position_info(symbol)
        if not position:
            entry_price = helper.get_market_entry_price(symbol)
            if entry_price is None:
                print(" >> [ERROR] Orderbook에서 진입할 금액 정보를 가져오지 못함")
                continue
            helper.place_order(symbol, entry_price, qty)

        position = helper.get_position_info(symbol)
        if position is None:
            continue

        avg_price = float(position["avgPrice"])
        mark_price = float(position["markPrice"])
        leverage = float(position["leverage"])
        size = float(position["size"])
        profit_rate = helper.get_profit_rate(avg_price, mark_price, leverage)
        print(
            f" >> [DEBUG] Long, {profit_rate:.2f}% (Size: {size}), 현재가/진입가: {mark_price}/{avg_price}")

        # 조건에 맞으면 추가 진입
        additional_base_amount = qty * 3
        for i in range(1, 12):
            if size <= additional_base_amount * i and profit_rate <= -10 * (i + 1):
                entry_price = helper.get_market_entry_price(symbol)
                if entry_price is None:
                    print(" >> [ERROR] Orderbook에서 진입할 금액 정보를 가져오지 못함")
                    continue
                helper.place_order(symbol, entry_price, next_qty)
                break

        # 급등해서 TP 설정 전에 TP 이상 오르면 주문 접수가 안됨. 그때는 5%씩 올려서 TP 설정.
        for i in range(6):
            percent = 0.1 + (i * 0.05)
            try:
                take_profit = helper.get_take_profit(avg_price, percent / leverage)
                print(f" >> [INFO] TP 설정. {percent}% / 설정 금액: {take_profit}")
                helper.set_take_profit(symbol, take_profit)
                break
            except Exception as e:
                print(f" >> [WARN] TP 설정 실패. 다음 퍼센트 값으로 설정 시도. err: {e}")
                helper.sleep()


if __name__ == "__main__":
    main()
