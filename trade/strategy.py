# -*- coding: utf-8 -*-

from core.bybit_helper import BybitHelper
from utils.config import get_config


class TradeStrategy:
    @classmethod
    def infinit(cls):
        bybit_config = get_config()["bybit"]
        helper = BybitHelper(config=bybit_config)
        symbols = helper.get_target_symbols()
        krw = helper.get_max_entry_price(len(symbols))

        for symbol in symbols:
            print(f"-*-*- {symbol} 매매 시작 -*-*-")

            helper.cancel_all_orders(symbol)

            qty, next_qty = helper.get_entry_qty(symbol, krw)
            print(f" >> [DEBUG] 첫 진입 개수: {qty}, 추가 진입 개수: {next_qty}")

            position = helper.get_position_info(symbol)
            if not position:
                entry_price = helper.get_market_entry_price(symbol)
                if entry_price is None:
                    print(" >> [ERROR] Orderbook에서 진입할 금액 정보를 가져오지 못함")
                    continue
                helper.place_order(symbol, "Buy", entry_price, qty)
                print(f" >> [INFO] 첫 진입 완료: Long {qty} @ {entry_price}")

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
                    print(
                        f" >> [DEBUG] 진입한 qty가 {additional_base_amount * i} 이하이고, 수익률이 {-10 * (i + 1)}% 이하 만족하여 추가 진입 시도")
                    helper.place_order(symbol, "Buy", entry_price, next_qty)
                    print(f" >> [INFO] 추가 진입 완료: Long {next_qty} @ {entry_price}")
                    break

            # 지정가 매도 설정 시도
            percent = 0.1
            position = helper.get_position_info(symbol)
            total_qty = float(position["size"])
            avg_price = float(position["avgPrice"])
            take_profit_price = helper.get_take_profit_price(avg_price, percent / leverage)
            print(f" >> [INFO] 포지션 종료 지정가 설정. {percent}% / 설정 금액: {take_profit_price}")
            helper.place_order(symbol, "Sell", take_profit_price, total_qty)
            helper.sleep()

            # 급등해서 매도 설정 안되면 TP로 판매하기 위한 방어로직
            for i in range(1, 5):
                percent = 0.1 + (i * 0.05)
                take_profit_price = helper.get_take_profit_price(avg_price, percent / leverage)
                print(f" >> [INFO] TP 설정. {percent}% / 설정 금액: {take_profit_price}")
                if helper.set_take_profit(symbol, take_profit_price):
                    break
                else:
                    # TP 설정 실패하면 profit 5% 올려서 다시 시도
                    print(f" >> [WARN] TP 설정 실패. 다음 퍼센트 값으로 설정 시도.")
                    helper.sleep()
