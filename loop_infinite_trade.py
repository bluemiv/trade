# -*- coding: utf-8 -*-

from trade.strategy import TradeStrategy
from utils.decorator import loop_decorator


@loop_decorator(loop_time=2 * 60)
def main():
    TradeStrategy.infinit()


if __name__ == "__main__":
    main()
