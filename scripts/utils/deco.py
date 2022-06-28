# -*- coding: utf-8 -*-

import time
import traceback


def ignore_error_deco(func):
    """에러를 무시하는 데코레이터"""

    def wrapper_func(cls):
        try:
            return func(cls)
        except Exception as e:
            print(traceback.format_exc())

    return wrapper_func


def infinity_trade(timer=60 * 15):
    """무한 반복 실행하는 데코레이터"""

    def ignore_error_deco(func):
        def wrapper_func(cls):
            while True:
                try:
                    func(cls)
                except Exception as e:
                    print(traceback.format_exc())
                finally:
                    print("sleep {}sec".format(timer))
                    time.sleep(timer)

        return wrapper_func

    return ignore_error_deco
