import copy


class MyList:
    """
    A container object that emulates the behaviour of a pythonic list.
    Each member in the list would be a ListMember object.
    The MyList object holds a direct pointer to the first and last member in the list, and
    each ListMember holds a direct pointer to the proceeding ListMember object.
    """
    def __init__(self):
        """
        Initiates a MyList object.
        """
        self.first_member = None
        self.last_member = None
        self.list_length = 0

    def append(self, value):
        """
        Creates a new ListMember and adds it to the list.

        :param value: The value that would be held in the ListMember.
        """
        if self.first_member is None:
            self.first_member = ListMember(value)
            self.last_member = self.first_member
        else:
            self.last_member.next_member = ListMember(value)
            self.last_member = self.last_member.next_member
        self.list_length += 1

    def __len__(self)-> int:
        return self.list_length

    def __iter__(self):
        """
        Initiates and returns an Iterator object that allows iterating over the list members.

        :return: A Iterator object.
        """
        return ListIterator(self)

    def remove(self, value_to_remove):
        """
        Removes the first ListMember that holds the given value.

        :param value_to_remove: A value that would be removed from the list.
        """
        if self.list_length == 0:
            raise ValueError('MyList.remove(x): x not in list')

        for member in self:
            if member.value == value_to_remove or member.next_member.value == value_to_remove:
                member_to_modify = member
                break
            elif member is self.last_member:
                raise ValueError('MyList.remove(x): x not in list')

        if member_to_modify is self.first_member:
            if self.list_length == 1:
                self.first_member = None
                self.last_member = None
            else:
                self.first_member = self.first_member.next_member

        else:
            if member_to_modify.next_member is self.last_member:
                self.last_member = member_to_modify
                member_to_modify.next_member = None
            else:
                member_to_modify.next_member = member_to_modify.next_member.next_member

        self.list_length -= 1

    def __str__(self)-> str:
        """
        Returns a textual representation of the list.

        :return: A string representing the list.
        """
        return '[{}]'.format(','.join(str(member.value) for member in self))

    def __add__(self, other):
        """
        Adds one MyList object to another and returns a new MyList object comprised of the two.

        :param other: The second MyList object we want to add to the current one.
        :return: A new MyList object containing the values of both the lists.
        """
        if type(other) is not MyList:
            raise TypeError("Can only concatenate MyList  object to another MyList object")
        copy_of_first_list = copy.deepcopy(self)
        copy_of_second_list = copy.deepcopy(other)
        copy_of_first_list.last_member.next_member = copy_of_second_list.first_member
        copy_of_first_list.last_member = copy_of_second_list.last_member
        return copy_of_first_list

    def __getitem__(self, key):
        if type(key) is not int:
            raise TypeError("Keys must be integers")
        if key < 0 or key > self.list_length - 1:
            raise KeyError("Key out of range")
        else:
            for index, member in enumerate(self):
                if index == key:
                    return member.value


class ListIterator:
    """
    A Iterator for MyList objects.
    """
    def __init__(self, list_object):
        """
        Initiates the ListIterator.
        :param list_object:
        """
        self.list = list_object
        self.current_iteration_object = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_iteration_object is None:
            self.current_iteration_object = self.list.first_member
        else:
            self.current_iteration_object = self.current_iteration_object.next_member

        if self.current_iteration_object is not None:
            return self.current_iteration_object
        else:
            raise StopIteration


class ListMember:
    """
    A member of a MyList series.
    """
    def __init__(self, value):
        """
        Initiates the ListMember and sets the value it holds.
        :param value: The vale that should be held in the member.
        """
        self.value = value
        self.next_member = None


def main():
    my_list = MyList()
    print("Empty List")
    print(my_list)
    my_list.append(1)
    my_list.append(2)
    my_list.append(3)
    print("List with 3 elements")
    print(my_list)
    my_list.remove(3)
    print("Removed 3")
    print(my_list)
    my_list2 = MyList()
    my_list2.append(3)
    my_list2.append(4)
    my_list2.append(5)
    print("A second List")
    print(my_list2)
    print("Add the second list to the first list")
    print(my_list + my_list2)
    print("my_list[2]")
    print(my_list2[0])


if __name__ == '__main__':
    main()
