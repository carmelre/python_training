from functools import partial
import time


def timer(func):
    """
    A generator that executes a function and yields a moving average of the function runtime.
    :param func: The function that would be tested.
    :return: Average runtime.
    """
    runtime_stats = {'sum_of_run_times': 0, 'number_of_executions': 0}
    rounds = None
    while True:
        if rounds is None:
            rounds = 1
        for cycle in range(rounds):
            start_time = time.monotonic()
            func()
            elapsed_time = time.monotonic() - start_time
            runtime_stats['sum_of_run_times'] += elapsed_time
        runtime_stats['number_of_executions'] += rounds
        rounds = yield runtime_stats['sum_of_run_times'] / runtime_stats['number_of_executions']


def slow_func_with_arguments():
    def general_func(*args, **kwargs):
        return sum(args) + sum([value for value in kwargs.values()])
    return partial(general_func, 1, 2, kwarg1=3, kwarg2=4)


if __name__ == '__main__':
    g = timer(slow_func_with_arguments)
    print(next(g))
    g.send(2)
    print(next(g))
    print(next(g))


