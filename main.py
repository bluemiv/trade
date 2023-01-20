# -*- coding: utf-8 -*-

from strategy import infinity
from strategy import rsi

st = [
    {"idx": 0, "label": "무한매매", "func": infinity.Infinity().run},
    {"idx": 1, "label": "RSI 매매", "func": rsi.Rsi().run}
]

if __name__ == '__main__':
    choice = '\n'.join(list(map(lambda x: f"{x['idx']}. {x['label']}", st)))
    num = input(f"매매 전략 선택\n{choice}\n > ")
    st[int(num)]["func"]()
