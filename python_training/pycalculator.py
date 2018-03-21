

class Calculator:
    def __init__(self):
        self.saved_num = None

    def add(self, a, b):
        self.check_input(a, b)
        return a + b

    def subtract(self, a, b):
        self.check_input(a, b)
        return a - b

    def divide(self, a, b):
        self.check_input(a, b)
        return a / b

    def multiply(self, a, b):
        self.check_input(a, b)
        return a * b

    def get_saved_number(self):
        return self.saved_num

    def set_saved_num(self, number):
        self.check_input(number)
        self.saved_num = number

    @staticmethod
    def check_input(*args):
        if any([arg for arg in args if type(arg) is not int]):
                raise TypeError


