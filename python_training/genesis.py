WORD_LIST = sorted(['precede', 'border', 'legs', 'alert', 'blood', 'group', 'unlock', 'loutish', 'measly', 'angle',
                    'filthy', 'son', 'competition', 'zippy', 'mighty', 'shy', 'unknown', 'famous', 'minister', 'anger'])


def word_generator(pointer=''):
    """
    Generates words from a sorted word list. If a value is sent to the generator,
    the next word that is alphabetically bigger than the value is returned.

    :param pointer: If given, the generator will start returning words that are bigger than this value.
    :return: The next word in the word list that is bigger tham the pointer.
    """
    while True:
        pointer = get_next_bigger_value(pointer, WORD_LIST)
        if pointer is None:
            raise StopIteration('There are no more words in the list')
        user_pointer = yield pointer
        if user_pointer:
            pointer = user_pointer


def get_next_bigger_value(comparison_value, array) -> str:
    """
    Iterates over a list and returned the first value that is bigger than the value we compare to.

    :param comparison_value: The value which the items in the list will be compared to.
    :param array: The list that would be iterated over.
    :return: The first value that is bigger than the compared value.
    """
    for value in array:
        if value > comparison_value:
            return value


def main():
    word_gen = word_generator()
    for i in range(5):
        print(next(word_gen))
        if i == 1:
            word_gen.send('m')


if __name__ == '__main__':
    main()
