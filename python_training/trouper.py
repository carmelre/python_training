
class Number(int):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.dividers = [1, number]
        self._get_all_dividers()

    def _get_all_dividers(self):
        """
        Appends to the dividers list the rest of the numbers dividers(that are not 1 or the number itself)
        """
        for i in range(2, int(self.number**0.5) + 1):
            if self.number % i == 0:
                self.dividers += [i, int(self.number/i)]
        self.dividers.sort()

    def __contains__(self, item):
        return True if item in self.dividers else False

    def __getitem__(self, item):
        return self.dividers[item]


def main():
    num = Number(18)
    print(num.dividers)
    print(num[1])
    print(num[1:5])


if __name__ == '__main__':
    main()



