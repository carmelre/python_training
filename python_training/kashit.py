from functools import wraps
from collections import namedtuple


def save_results(original_func):
    """
    The decorator creates a mapping between sets of arguments that were used in the past,
    and the result they have produced.
    Whenever the function is called the arguments are searched for in the mapping,
    and if they exist the result is returned without performing the calculation again.
    """
    args_and_result_list = []
    ArgumentsAndResults = namedtuple('ArgumentsAndResults', ['args', 'kwargs', 'result'])

    @wraps(original_func)
    def wrapper(*args, **kwargs):
        nonlocal args_and_result_list
        pre_calculated_result = [item.result for item in args_and_result_list
                                 if item.args == args and item.kwargs == kwargs]
        if len(pre_calculated_result) != 0:
            return pre_calculated_result[0]
        else:
            new_result = original_func(*args, **kwargs)
            args_and_result_list.append(ArgumentsAndResults(args, kwargs, new_result))
            return new_result

    return wrapper


@save_results
def heavy_func(*args, **kwargs):
    return sum(args) + sum(kwargs.values())


def main():
    print(heavy_func(1, 2, 3, bla=4, bla2=5))
    print(heavy_func(1, 2, 3, bla=4, bla2=5))


if __name__ == '__main__':
    main()
