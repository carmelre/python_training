
class MyList:
    """
    Creates a series of objects that mimic a pythonic list.
    Each object holds a value, and a pointer to the next item of the list.
    The user accesss the list through the first item.
    The first initiation of the class (by the user) creates an empty list, and items are added by calling the append
    method.
    """
    def __init__(self, index=0, value=None):
        """
        Creates a list member that holds a specific value of the list, and points to the next value.
        At first self.next_value is empty, until the append method is called.
        :param index: The index of the item in the series
        :param value: The value in the series that the specific MyList object represents.
        """
        self.value = value
        self.next_value = None
        self.index = index

    def append(self, appended_value):
        """
        Appends a value to the series. If empty, the value of the current object would be set.
        Otherwise, the method would be called upon the next object.
        :param appended_value: The value that would be added to the series.
        """
        if self.value is None:
            self.value = appended_value
        elif self.next_value is None:
            self.next_value = (MyList(self.index + 1, appended_value))
        else:
            self.next_value.append(appended_value)

    def __len__(self)-> int:
        """
        Calculates the number of objects in the series.
        :return: The number of objects in the series.
        """
        return self._get_last_index() + 1

    def _get_last_index(self)->int:
        """
        Finds out what is the index of the last object in the series.
        :return: The index of the last object.
        """
        if self.next_value is None:
            last_index = self.index
        else:
            last_index = self.next_value._get_last_index()
        return last_index

    def remove(self, value_to_remove):
        """
        Remove a value from the series.
        :param value_to_remove: The value that will be removed from the series.
        """
        if self.value == value_to_remove:
            # Erase the value of a single item series.
            if self.next_value is None:
                self.value = None
                return
            # We remove the value from the series by copying the values of the next item, and pointing to the one after.
            # Afterwards we reduce by 1 all the indexes of the next items in the series.
            else:
                self.value = self.next_value.value
                self.next_value = self.next_value.next_value
                self._reduce_index_of_next_items()
                return

        if self.next_value is not None:
            # In this block we cover the situation in which the value that should be removed is the last.
            if self.next_value.value == value_to_remove and self.next_value.next_value is None:
                self.next_value = None
                return
            # If the current class doesnt contain the wanted value, proceed to the next one.
            else:
                self.next_value.remove(value_to_remove)
        # Raise a value error if we have reached the last object in the series, and it doesnt contain the wanted value.
        if self.index == self._get_last_index():
            raise ValueError('MyList.remove(x): x not in list')

    def _reduce_index_of_next_items(self):
        """
        Reduces the indices of the next objects by one.
        """
        if self.next_value is not None:
            self.next_value.index -= 1
            self.next_value._reduce_index_of_next_items()

    def __str__(self):
        """
        Returns a string that represents the series.
        :return: A string that mimics the string representation of a pythonic list: [ item1, item2, item3...].
        """
        return "[{}]".format(self._get_str_value_of_next_items())

    def _get_str_value_of_next_items(self)->str:
        """
        Returns a string that combines all the items of the series, separated by comas.
        "item1,item2,tem3..."
        :return: The concatenated string.
        """
        if self.value is None:
            return ""
        else:
            if self.next_value is not None:
                return f"{self.value}, {self.next_value._get_str_value_of_next_items()}"
            else:
                return self.value

    def __add__(self, other):
        """
        Concatenates two MyList series.
        :param other: The series that would be added to the current MyList series.
        """
        if type(other) is not type(self):
            raise TypeError("Can only concatenate MyList  object to another MyList object")
        else:
            if self.next_value is None:
                self.next_value = other
            else:
                self.next_value.__add__(other)
