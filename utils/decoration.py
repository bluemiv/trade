# -*- coding: utf-8 -*-

import time
import traceback


def ignore_error_deco(func):
    """에러 무시"""

    def wrapper_func(cls):
        try:
            return func(cls)
        except Exception as e:
            print(traceback.format_exc())

    return wrapper_func


def forever(timer=15 * 60):
    """무한 반복 실행"""

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
