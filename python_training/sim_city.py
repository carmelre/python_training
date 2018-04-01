BASE_MUNICIPALITY_TAX_RATE = 1000


class Ackland:
    """
    The state Ackland itself.
    """

    def __init__(self, cities):
        """
        Initiates the Ackland state object.
        """
        if isinstance(cities, City):
            cities = [cities]
        self.cities = cities

    def calculate_total_tax_amount(self) -> int:
        """
        Calculates the amount of tax money that would be earned from all the cities of Ackland.

        :return: The total amount of tax money from all the cities of the state.
        """
        return sum([city.how_much_money() for city in self.cities])


class City:
    """
    A city in Ackland.
    """

    def __init__(self, city_name):
        """
        Initiates a new City object.

        :param city_name: The name of the city you would like to create.
        """
        self.city_name = city_name
        self.base_municipality_tax_rate = BASE_MUNICIPALITY_TAX_RATE
        self.neighbourhoods = {}

    def how_much_money(self) -> int:
        """
        Calculates the concluded amount of tax money that would be payed by The cities in Ackland.

        :return: The amount of money that should be payed.
        """
        return self.base_municipality_tax_rate + sum([neighbourhood.get_neighbourhood_tax_rate() for neighbourhood
                                                      in self.neighbourhoods.values()])

    def ruin_a_neighbourhood(self, neighbourhood_name):
        """
        Removes a neighbourhood from the city.

        :param neighbourhood_name: The name of the neighbourhood that would be removed.
        """
        self._verify_neighbourhood(neighbourhood_name)
        self.base_municipality_tax_rate *= 1.05
        self.neighbourhoods.pop(neighbourhood_name)

    def build_a_neighbourhood(self, neighbourhood_name):
        """
        Adds a neighbourhood to the city.

        :param neighbourhood_name: The name of the neighbourhood.
        :return A neighbourhood object if succeeded, None otherwise.
        """
        self._verify_neighbourhood(neighbourhood_name, should_exist=False)
        self.base_municipality_tax_rate *= 1.1
        self.neighbourhoods[neighbourhood_name] = neighbourhood(neighbourhood_name)
        return self.neighbourhoods[neighbourhood_name]

    def build_a_house(self, neighbourhood_name, number_of_family_members, size_of_house):
        """
        Adds a house to a neighbourhood.

        :param neighbourhood_name: The neighbourhood that a house would be added to.
        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        self._verify_neighbourhood(neighbourhood_name)
        self.neighbourhoods[neighbourhood_name].add_house(number_of_family_members, size_of_house)

    def build_a_park(self, neighbourhood_name):
        """
        Adds a park to a neighbourhood.

        :param neighbourhood_name: The name of the neighbourhood to which the park would be added.
        """
        self._verify_neighbourhood(neighbourhood_name)
        self.neighbourhoods[neighbourhood_name].add_park()

    def _verify_neighbourhood(self, neighbourhood_name, should_exist=True):
        """
        Verifies that the neigborhood exists if should_exist= True, verifies that it doesnt exist otherwise.
        :param should_exist:
        :param neighbourhood_name: The neighbourhood name that would be verified.
        """
        if should_exist:
            if neighbourhood_name in self.neighbourhoods:
                return
            raise KeyError(f'The neighbourhood {neighbourhood_name} doesnt exist in {self.city_name}')
        else:
            if neighbourhood_name not in self.neighbourhoods:
                return
            raise KeyError(f'The neighbourhood {neighbourhood_name} already exist in {self.city_name}')


class neighbourhood:
    """
    A neighbourhood in Ackland (part of a City).
    """

    def __init__(self, name, number_of_parks=0, *houses):
        """
        Initiates a new neighbourhood object.

        :param name: The name of the neighbourhood.
        :param number_of_parks: The number of parks in the neighbourhood.
        :param houses: The number of houses in the neighbourhood.
        """
        self.name = name
        self.number_of_parks = number_of_parks
        self.houses = list(houses)

    def get_neighbourhood_tax_rate(self) -> int:
        """
        Calculates the amount of tax money that should be payed by the neighbourhood, combining the amount payed by
        the neighbourhood committee and each of the houses in the neighbourhood.

        :return: The amount of money that should be payed by the neighbourhood.
        """
        return self.base_neighbourhood_tax_rate + sum([house.get_house_tax_rate() for house in self.houses])

    @property
    def base_neighbourhood_tax_rate(self) -> int:
        """
        Calculates the amount of tax money that should be payed by the neighbourhood committee.

        :return: The amount of money that should be payed by the committee.
        """
        return 5 * self.number_of_parks + 3 * len(self.houses)

    def build_house(self, number_of_family_members, size_of_house):
        """
        Adds a house to the neighbourhood.

        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        self.houses.append(House(number_of_family_members, size_of_house))

    def build_park(self):
        """
        Adds a park to the neighbourhood.
        """
        self.number_of_parks += 1


class House:
    """
    A house in Ackland (part of a neighbourhood).
    """

    def __init__(self, number_of_family_members, size_of_house):
        """
        Initiates a new house object.

        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        self.number_of_family_members = number_of_family_members
        self.size_of_house = size_of_house

    def get_house_tax_rate(self) -> int:
        """
        Calculates the amount of tax money that should be payed by the house.

        :return: The amount of money that should be payed by the house.
        """
        return self.size_of_house * self.number_of_family_members


def main():
    shenkler_city = City('shenklers_city')
    shenkler_neighbourhood_1 = shenkler_city.build_a_neighbourhood('Shenkler')
    shenkler_neighbourhood_1.build_house(1, 1)
    shenkler_neighbourhood_1.build_house(2, 1)
    shenkler_neighbourhood_2 = shenkler_city.build_a_neighbourhood('Shenkler2')
    shenkler_neighbourhood_2.build_house(1, 1)
    shenkler_neighbourhood_2.build_house(2, 1)
    print('Shenkler City tax rate (expected 1128):', shenkler_city.how_much_money())
    benor_city = City('benors_city')
    benor_neighbourhood1 = benor_city.build_a_neighbourhood('Benor')
    benor_neighbourhood1.build_park()
    benor_neighbourhood2 = benor_city.build_a_neighbourhood('Benor2')
    benor_neighbourhood2.build_park()
    print('Benor City tax rate (expected 1120)', benor_city.how_much_money())
    benor_city.ruin_a_neighbourhood('Benor')
    print('Benor City tax rate after ruining Benor neighbourhood (expected 1175)', benor_city.how_much_money())
    ackland = Ackland([shenkler_city, benor_city])
    print('Total tax in ackland: expected 2503.5', ackland.calculate_total_tax_amount())


if __name__ == '__main__':
    main()
