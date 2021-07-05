import math

class Number(int):
    """
    An object that extends the int object and adds functionality over the dividers of a number.
    """

    def __init__(self, number):
        """
        Instantiates a number object and prepares the dividers list.

        :param number:
        """
        super().__init__()
        self.number = number
        self.dividers = [1, number]
        self._get_all_dividers()

    def _get_all_dividers(self):
        """
        Appends to the dividers list the rest of the numbers dividers(that are not 1 or the number itself).
        """
        square_root = self.number ** 0.5
        for i in range(2, int(square_root) + 1):
            if self.number % i == 0:
                self.dividers += [i, int(self.number / i)]
        if square_root.is_integer():
            self.dividers.remove(square_root)
        self.dividers.sort()

    def __contains__(self, item):
        return True if item in self.dividers else False

    def __getitem__(self, item):
        return self.dividers[item]


def main():
    num = Number(16)
    print(num.dividers)
    print(num[1])
    print(num[1:4])


if __name__ == '__main__':
    main()
