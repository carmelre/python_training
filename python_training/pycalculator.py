def check_input(original_func):
    def wrapper(*args):
        if any([True for arg in args[1:] if not (type(arg) is int or type(arg) is float)]):
            raise TypeError("The given parameters are not all integers")
        else:
            return original_func(*args)
    return wrapper


class Calculator:
    def __init__(self):
        self.saved_num = None

    @check_input
    def add(self, a, b):
        return a + b

    @check_input
    def subtract(self, a, b):
        return a - b

    @check_input
    def divide(self, a, b):
        return a / b

    @check_input
    def multiply(self, a, b):
        return a * b

    def get_saved_number(self):
        return self.saved_num

    @check_input
    def set_saved_num(self, number):
        print(number)
        self.saved_num = number