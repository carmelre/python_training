from python_training import fast
import time


def test_send_number_of_executions_to_generator(mocker):
    mocked_func = mocker.patch.object(fast, 'slow_func_with_arguments')
    generator = fast.timer(mocked_func)
    next(generator)
    generator.send(2)
    next(generator)
    assert mocked_func.call_count == 4


def test_correct_runtime():
    start_time = time.monotonic()
    fast.slow_func_with_arguments()
    elapsed_time = time.monotonic() - start_time
    generator = fast.timer(fast.slow_func_with_arguments())
    assert round(elapsed_time, 2) == round(next(generator), 2)


def test_correct_runtime_with_send_to_generator():
    start_time = time.monotonic()
    fast.slow_func_with_arguments()
    elapsed_time = time.monotonic() - start_time
    generator = fast.timer(fast.slow_func_with_arguments())
    next(generator)
    generator.send(3)
    assert round(elapsed_time, 2) == round(next(generator), 2)