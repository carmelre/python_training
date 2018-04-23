from functools import partial
import time
import timeit


def timer(func):
    runtime_avg = None
    while True:
        # define the number of runs




def super_slow_func(sleep_time):
    time.sleep(sleep_time)


if __name__ == '__main__':
    slow_func_with_arguments = partial(super_slow_func, sleep_time=1)
    timeit.timeit()
