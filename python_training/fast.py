from functools import partial
import time


def timer(func):



def super_slow_func(sleep_time):
    time.sleep(sleep_time)


if __name__ == '__main__':
    slow_func_with_arguments = partial(super_slow_func, sleep_time=1)

