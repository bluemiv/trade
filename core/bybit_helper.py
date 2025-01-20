# -*- coding: utf-8 -*-

import time
from pybit.unified_trading import HTTP


class BybitHelper:
    def __init__(self, config):
        self.client = HTTP(api_key=config["api_key"], api_secret=config["api_secret"])
        self.sleep_time = config["sleep_time"]
        self.price = config.get("price")
        self.exchange = config["exchange"]
        self.targets = config["targets"]

    def get_target_symbols(self):
        """
        트레이딩을 할 코인 종목을 반환 (중복 제거)
        :return: 트레이딩 종목 리스트
        """
        return list(set(self.targets))

    def cancel_all_orders(self, symbol):
        """
        입력받은 symbol의 주문 건을 모두 취소한다.
        :param symbol: 대상 symbol
        :return: None
        """
        try:
            self.client.cancel_all_orders(category="linear", symbol=symbol)
            print(f" >> [INFO] {symbol} 모든 주문 취소 완료")
        except Exception as e:
            print(f" >> [ERROR] 주문 취소 실패: {e}")

    def get_orderbook(self, symbol):
        """symbol의 Orderbook 반환한다
        :param symbol: 대상 symbol
        :return: orderbook (오류 발생시 None)
        """
        try:
            orderbook = self.client.get_orderbook(category="linear", symbol=symbol)
            self.sleep()
            return orderbook
        except Exception as e:
            print(f" >> [ERROR] Orderbook 조회 실패: {e}")
            return None

    def get_entry_qty(self, symbol, krw):
        """입력받은 symbol의 진입할 코인 개수를 반환한다.
        :param symbol: 대상 symbol
        :param krw: 진입할 금액
        :return: (첫번째 진입 개수, 이후 추가 진입 개수)
        """

        def get_valid_amount(amount):
            return int(amount * 10) / 10 if amount <= 3 else int(amount)

        orderbook = self.get_orderbook(symbol)
        if not orderbook:
            return 0, 0

        coin_price = float(orderbook["result"]["b"][0][0])
        price = int(krw if self.price is None else self.price)
        if self.price is None:
            print(f" >> [DEBUG] 설정된 진입 금액이 없어, 자동으로 금액 설정. 진입 금액: {price}원")
        dollar = price / self.exchange
        dollar = dollar if dollar > 5.5 else 5.5
        half_dollar = (dollar / 2) if (dollar / 2) > 5.5 else 5.5
        return get_valid_amount(dollar / coin_price), get_valid_amount(half_dollar / coin_price)

    def get_position_info(self, symbol):
        """현재 포지션 정보를 반환한다.
        :param symbol: 대상 symbol
        :return: 포지션 정보 (없거나 오류 발생시 None)
        """
        try:
            response = self.client.get_positions(category="linear", symbol=symbol)
            positions = response.get("result", {}).get("list", [])
            for position in positions:
                if float(position["size"]) > 0:  # 포지션이 있는 경우만
                    return position
            return None
        except Exception as e:
            print(f" >> [ERROR] 포지션 조회 실패: {e}")
            return None

    def get_market_entry_price(self, symbol):
        """
        Orderbook에서 진입할 금액을 가져온다.
        :param symbol: 대상 symbol
        :return: 현재 Orderbook 기준으로 진입할 금액 (오류 발생시 None)
        """
        orderbook = self.get_orderbook(symbol)
        if orderbook:
            best_bid = float(orderbook["result"]["b"][0][0])
            return best_bid
        return None

    def place_order(self, symbol, side, price, qty):
        """
        Long 주문 접수
        :param symbol: 대상 symbol
        :param price: 주문할 시장 가격
        :param qty: 포지션 개수
        :return:
        """
        try:
            self.client.place_order(
                category="linear",
                symbol=symbol,
                side=side,  # "Buy", "Sell"
                orderType="Limit",
                qty=qty,
                price=price,
                timeInForce="PostOnly",
                positionIdx=1  # Hedge mode
            )
            return True
        except Exception as e:
            print(f" >> [ERROR] 주문 접수 실패: Long {qty} @ {price} / err: {e}")
            return False

    def sleep(self):
        """딜레이"""
        time.sleep(self.sleep_time)

    def get_profit_rate(self, entry_price, mark_price, leverage):
        """레버리지 고려해서 현재 수익률 계산해서 반환
        (e.g. -1%, x10 => -10%)
        :param entry_price: 진입한 가격
        :param mark_price: 현재 시장가
        :param leverage: 레버리지 값
        :return: 레버리지 고려한 현재 수익률
        """
        return (((mark_price - entry_price) / entry_price) * leverage) * 100

    def get_take_profit_price(self, entry_price, profit_ratio):
        """TP 가격 반환"""
        return entry_price * (1 + profit_ratio)

    def set_take_profit(self, symbol, take_profit):
        """TP를 설정한다.

        :param symbol: 대상 symbol
        :param take_profit: 설정할 TP 값
        :return: 설정 성공하면 True 반환. 실패하면 False 반환
        """
        try:
            self.client.set_trading_stop(
                category="linear",
                symbol=symbol,
                takeProfit=str(take_profit),
                tpTriggerBy="MarkPrice",
                tpslMode="Full",
                positionIdx=1,  # Hedge Mode
            )
            print(f" >> [INFO] TP 설정 완료: {take_profit}")
            return True
        except Exception as e:
            print(f" >> [ERROR] TP 설정 실패: {e}")
            return False

    def get_max_entry_price(self, coin_len):
        try:
            wallet_balance = self.client.get_wallet_balance(accountType="UNIFIED")
            wallet = list(filter(lambda x: x["accountType"] == "UNIFIED", wallet_balance["result"]["list"]))[0]
            usdt = float(wallet["totalEquity"]) / coin_len * 1.5
            krw = usdt * self.exchange
            print(f" >> [INFO] 최대 권장 금액: {usdt} USD / {krw} KRW")
            self.sleep()
            return krw
        except Exception as e:
            print(f" >> [ERROR] 자산 조회 실패: {e}")
