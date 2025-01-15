# -*- coding: utf-8 -*-

import time


def loop_decorator(loop_time=2 * 60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                    print(f"\nDelay {loop_time}\n")
                    time.sleep(loop_time)
                except Exception as e:
                    print(f"ERROR. err: {e}")

        return wrapper

    return decorator
