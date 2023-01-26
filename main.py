# -*- coding: utf-8 -*-

from strategy import auto_seller
from strategy import infinity
from strategy import rsi
from strategy import seed

st = [
    {"idx": 0, "label": "무한매매", "obj": infinity.Infinity},
    {"idx": 1, "label": "RSI 매매", "obj": rsi.Rsi},
    {"idx": 2, "label": "자동 매도", "obj": auto_seller.AutoSeller},
    {"idx": 3, "label": "농부 매매", "obj": seed.Seed}
]

if __name__ == '__main__':
    choice = '\n'.join(list(map(lambda x: f"{x['idx']}. {x['label']}", st)))
    num = input(f"매매 전략 선택\n{choice}\n > ")
    st[int(num)]["obj"]().run()
