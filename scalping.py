# -*- utf-8 -*-
import math
import os
import json
import time

import pyupbit

MIN_BUY_PRICE = 5050


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


def get_rsi(symbol, interval='minute1', period=14):
    """
    RSI 값을 반환한다.
    - day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
    - (일봉/1분봉/3분봉/5분봉/10분봉/15분봉/30분봉/60분봉/240분봉/주봉/월봉)
    """
    df = pyupbit.get_ohlcv(symbol, interval=interval, count=250)

    delta = df['close'].diff()
    delta = delta[1:]

    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0).abs()

    avg_gain = gain.ewm(alpha=1 / period).mean()
    avg_loss = loss.ewm(alpha=1 / period).mean()

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.iloc[-1]


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

    info = get_balance_info(symbol)

    for unit in orderbook_units:
        balance_info = get_balance_info(symbol)
        remain_volume = float(balance_info["balance"])

        if remain_volume == 0:
            print(f"\t >> 더 이상 생성 가능한 매도 주문이 없습니다.")
            break

        trg_price = float(unit["ask_price"])
        volume = price / trg_price

        current_price = pyupbit.get_current_price(symbol)
        remain_price = float(info["balance"]) * current_price

        trg_volume = remain_volume if remain_price < price * 2 else volume
        upbit.sell_limit_order(symbol, trg_price, trg_volume)
        print(f"\t >> 매도 주문을 생성했습니다. price: {trg_price} volume: {trg_volume}")

        sleep()


def get_duplicate_price(orders):
    visited = {}
    results = []
    for order in orders:
        if order["side"] != "ask":
            continue

        price = order["price"]
        if visited.get(price, None) is not None:
            results.append(order)
            continue

        visited[price] = True

    return results


def cancel_buy_orders(symbol):
    """매수 주문을 모두 취소합니다."""
    orders = upbit.get_order(symbol)

    sell_order = get_duplicate_price(orders)
    buy_order = list(filter(lambda x: x["side"] == "bid", orders))
    buy_order.extend(sell_order)

    for order in buy_order:
        print(f"\t >> {order['side']}/{order['uuid']} 주문 취소")
        upbit.cancel_order(order['uuid'])
        sleep()


def get_my_coin_price(symbol):
    info = get_balance_info(symbol)
    balance = float(info["balance"]) + float(info["locked"])
    current_price = pyupbit.get_current_price(symbol)
    sleep()
    return balance * current_price


if __name__ == "__main__":
    print("[INFO] 프로그램 시작.")
    total_seed = get_my_total_seed()
    usable_seed = get_my_usable_seed()

    print(f"[INFO] 현재 나의 총 자산: {math.floor(total_seed)}원 / 가용 가능한 자산: {math.floor(usable_seed)}원")

    is_enable_buy = usable_seed > MIN_BUY_PRICE

    seed_divide = float(config["seed_divide"])
    price_atom = math.floor(total_seed / seed_divide)
    price_atom = price_atom if price_atom > MIN_BUY_PRICE else MIN_BUY_PRICE
    print(f"[INFO] 1매수 당 가격: {price_atom}원")

    for symbol in config["trade_symbols"]:
        print(f"\n[INFO] {symbol} 자동매매를 시작합니다.")
        print(f"\t >> 매수 주문을 초기화합니다.")
        cancel_buy_orders(symbol)

        period = 14
        rsi = get_rsi(symbol, period)
        print(f"\t >> 현재 1분봉 {period}분 주기의 RSI: {rsi}")

        # 1. 첫 매수
        balance = get_balance_info(symbol)
        not_exists_balance = balance is None
        if not_exists_balance:
            if rsi <= 60 and is_enable_buy:
                print("\t >> 보유한 자산이 없고, RSI가 60 이하이므로 첫 매수를 진행합니다.")
                buy_order(symbol, price_atom)
            continue

        profit_rate = get_profit_rate(symbol)
        coin_price = get_my_coin_price(symbol)
        print(f"\t >> 현재 보유한 코인의 원화 가치: {coin_price} / 수익률: {profit_rate}%")

        buy_addly_rate = (total_seed - usable_seed) / total_seed
        add_buy_rate = -0.3 - buy_addly_rate

        # 2. 추가 매수
        if (profit_rate < add_buy_rate or (coin_price < MIN_BUY_PRICE and rsi <= 60)) and is_enable_buy:
            print(f"\t >> 추가 매수 조건에 충족하여 매수를 진행합니다. buy rate: {add_buy_rate}")
            buy_order(symbol, price_atom)

        if profit_rate >= 0.3 and coin_price >= MIN_BUY_PRICE:
            print(f"\t >> 수익률이 0.3% 이상으로 매도 주문을 진행합니다.")
            sell_order(symbol, price_atom)
