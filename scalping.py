# -*- utf-8 -*-
import math
import sys
import os
import json
import time

import pyupbit


def get_config():
    config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())


config = get_config()
upbit = pyupbit.Upbit(config["access_key"], config["secret_key"])


def sleep():
    """API 호출 금지를 당하지 않도록 sleep을 수행"""
    time.sleep(float(config["sleep_time"]))


def get_my_total_seed():
    """원화, 코인 모든 자산의 평가 금액을 반환한다."""
    balances_info = upbit.get_balances()
    sleep()
    tickers = pyupbit.get_tickers()
    total_seed = 0
    for info in list(
            filter(lambda x: x["currency"] == "KRW" or "-".join([x["unit_currency"], x["currency"]]) in tickers,
                   balances_info)):
        if info["currency"] != "KRW":
            symbol = "-".join([info["unit_currency"], info["currency"]])
            current_price = pyupbit.get_current_price(symbol)
            total_seed += (float(info["balance"]) + float(info["locked"])) * current_price
            continue
        total_seed += float(info["balance"]) + float(info["locked"])
    return total_seed


def get_my_usable_seed():
    """트레이딩 가용 가능한 자산을 반환한다."""
    seed = upbit.get_balance("KRW")
    sleep()
    return seed


def get_balance_info(symbol):
    """특정 자산 정보를 반환한다."""
    balances_info = upbit.get_balances()
    sleep()
    for info in balances_info:
        cur_symbol = "-".join([info["unit_currency"], info["currency"]])
        if symbol == cur_symbol:
            return info
    return None


def get_rsi(symbol, period=14):
    """분봉 RSI 값을 반환한다"""
    df = pyupbit.get_ohlcv(symbol, interval="minute1", count=period)

    delta = df['close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi_list = 100 - (100 / (1 + rs))
    return rsi_list.iloc[-1]


def buy_order(symbol, price):
    """매수 주문 생성한다."""
    orderbook = pyupbit.get_orderbook(symbol)
    orderbook_units = orderbook['orderbook_units']
    trg_price = float(orderbook_units[0]["bid_price"])
    volume = price / trg_price
    upbit.buy_limit_order(symbol, trg_price, volume)
    print(f"\t >> 매수 주문을 생성했습니다. price: {trg_price} volume: {volume}")
    sleep()


def get_profit_rate(symbol):
    """수익률을 반환한다."""
    avg_price = upbit.get_avg_buy_price(symbol)
    current_price = pyupbit.get_current_price(symbol)
    profit_rate = (current_price - avg_price) / avg_price * 100
    sleep()
    return profit_rate


def sell_order(symbol, price):
    """매도 주문 생성한다."""
    orderbook = pyupbit.get_orderbook(symbol)
    orderbook_units = orderbook['orderbook_units']

    coin_price = get_my_coin_price(symbol)

    for unit in orderbook_units:
        balance_info = get_balance_info(symbol)
        remain_volume = float(balance_info["balance"])

        if remain_volume == 0:
            print(f"\t >> 더 이상 생성 가능한 매도 주문이 없습니다.")
            break

        trg_price = float(unit["ask_price"])
        volume = price / trg_price

        trg_volume = remain_volume if coin_price < price * 1.2 else volume
        upbit.sell_limit_order(symbol, trg_price, trg_volume)
        print(f"\t >> 매도 주문을 생성했습니다. price: {trg_price} volume: {trg_volume}")

        sleep()


def cancel_buy_orders(symbol):
    """매수 주문을 모두 취소합니다."""
    buy_order = list(filter(lambda x: x["side"] == "bid", upbit.get_order(symbol)))
    for order in buy_order:
        upbit.cancel_order(order['uuid'])
        sleep()


def get_my_coin_price(symbol):
    balance = float(upbit.get_balance(symbol))
    current_price = pyupbit.get_current_price(symbol)
    sleep()
    return balance * current_price


if __name__ == "__main__":
    print("[INFO] 프로그램 시작.")
    total_seed = get_my_total_seed()
    usable_seed = get_my_usable_seed()
    print(f"[INFO] 현재 나의 총 자산: {math.floor(total_seed)}원 / 가용 가능한 자산: {math.floor(usable_seed)}원")

    if usable_seed < 5050:
        print(f"[INFO] 거래 가능한 자산이 없습니다. seed: {usable_seed}")
        sys.exit()

    price_atom = math.floor(total_seed / 25)
    print(f"[INFO] 1매수 당 가격: {price_atom}원")

    for symbol in config["trade_symbols"]:
        print(f"\n[INFO] {symbol} 자동매매를 시작합니다.")
        print(f"\t >> 매수 주문을 초기화합니다.")
        cancel_buy_orders(symbol)

        balance = get_balance_info(symbol)
        not_exists_balance = balance is None

        period = 14
        rsi = get_rsi(symbol, period)
        print(f"\t >> 현재 1분봉 {period}분 주기의 RSI: {rsi}")

        if not_exists_balance:
            print(f"\t >> 보유한 자산이 없습니다. 매수를 시도합니다.")
            if rsi > 60:
                print("\t >> RSI가 60 초과로 매수를 진행하지 않습니다.")
            else:
                print("\t >> RSI가 60 이하이므로 매수를 진행합니다.")
                buy_order(symbol, price_atom)
        else:
            profit_rate = get_profit_rate(symbol)
            print(f"\t >> 현재 수익률: {profit_rate}%")

            coin_price = get_my_coin_price(symbol)

            if profit_rate < -0.3 or (coin_price < 5050 and rsi <= 60):
                print(f"\t >> 추가 매수 조건에 충족하여 매수를 진행합니다.")
                buy_order(symbol, price_atom)
            elif profit_rate > 0.3:
                print(f"\t >> 수익률이 0.3% 이상으로 매도 주문을 진행합니다.")
                sell_order(symbol, price_atom)
            else:
                print(f"\t >> 조건에 만족하지 않습니다. 매수/매도 주문을 수행하지 않습니다.")
