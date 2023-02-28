# -*- coding: utf-8 -*-
import time
import traceback

from bybit import bybit
from strategy import auto_seller
from strategy import infinity
from strategy import rsi
from strategy import seed
from utils import config_parser

if __name__ == '__main__':
    config = config_parser.get_config()
    platform = int(input("1. UPBIT\n2. BYBIT\n > "))
    if platform == 1:
        st = [
            {"idx": 0, "label": "무한매매", "obj": infinity.Infinity},
            {"idx": 1, "label": "RSI 매매", "obj": rsi.Rsi},
            {"idx": 2, "label": "자동 매도", "obj": auto_seller.AutoSeller},
            {"idx": 3, "label": "농부 매매", "obj": seed.Seed}
        ]
        choice = '\n'.join(list(map(lambda x: f"{x['idx']}. {x['label']}", st)))
        num = input(f"매매 전략 선택\n{choice}\n > ")
        st[int(num)]["obj"]().run()
    else:
        bybit_config = config["bybit"]
        bb = bybit.ByBit(bybit_config["api_key"], bybit_config["secret_key"])

        target_symbol = "STXUSDT"
        tick_usdt = 0.001
        timeout = 0.2

        while True:
            # short 포지션 초기화
            sell_order_list = bb.query_active_order(symbol=target_symbol)
            for sell_order in sell_order_list:
                order_id = sell_order["order_id"]
                try:
                    bb.cancel_active_order(symbol=target_symbol, order_id=order_id)
                    time.sleep(timeout)
                except Exception:
                    print(traceback.format_exc())

            position_list = bb.get_my_position(symbol=target_symbol)
            if len(position_list) == 0:
                cur_usdt = None
            else:
                cur_usdt = list(filter(lambda x: x["side"] == "Sell" and x["entry_price"] > 0, position_list))
                if len(cur_usdt) > 0:
                    cur_usdt = cur_usdt[0][
                        "entry_price"]
                else:
                    cur_usdt = None

            # 매수
            sell_list = list(filter(lambda x: x["side"] == "Sell", bb.get_order_book(symbol=target_symbol)))
            second = int(float(sell_list[20]["price"]) * 1000) / 1000
            if cur_usdt is None:
                init_usdt = second
            else:
                init_usdt = max(second, int((cur_usdt + 3 * tick_usdt) * 1000) / 1000) + tick_usdt

            for i in range(10):
                cur = round(init_usdt + (i + 1) * tick_usdt, 4)
                order = bb.open_short(target_symbol, 20, cur)
                time.sleep(timeout)

            # 매도 예약
            if cur_usdt is not None:
                my_position_list = bb.get_my_position(symbol=target_symbol)
                if len(position_list) != 0:
                    position = list(filter(lambda x: x["side"] == "Sell" and x["free_qty"] > 0, my_position_list))
                    if len(position) > 0:
                        position = position[0]
                        qty = position["free_qty"]

                        entry_price = position["entry_price"]
                        buy_list = list(filter(lambda x: x["side"] == "Buy", bb.get_order_book(symbol=target_symbol)))
                        market_price = float(buy_list[20]["price"])
                        init_usdt = min(market_price, entry_price) - tick_usdt
                        init_usdt = int(init_usdt * 1000) / 1000

                        cur_qty = 0
                        did_num = 4
                        for i in range(did_num):
                            cur_usdt = init_usdt - (i + 2) * tick_usdt

                            if cur_qty == 0:
                                cur_qty = int(qty / did_num)
                                qty = qty - cur_qty

                            if i == did_num - 1:
                                cur_qty = qty

                            bb.close_short(symbol=target_symbol, qty=cur_qty,
                                           price=cur_usdt)
                            time.sleep(timeout)

            time.sleep(5 * 60)
