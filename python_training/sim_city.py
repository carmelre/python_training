BASE_MUNICIPALITY_TAX_RATE = 1000


class Ackland:
    """
    The state Ackland itself.
    """

    def __init__(self, cities):
        """
        Initiates the Ackland state object.
        """
        if type(cities) is City:
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
        self.neighborhoods = {}

    def how_much_money(self) -> int:
        """
        Calculates the concluded amount of tax money that would be payed by The cities in Ackland.

        :return: The amount of money that should be payed.
        """
        return self.base_municipality_tax_rate + sum([neighborhood.get_neighborhood_tax_rate() for neighborhood
                                                      in self.neighborhoods.values()])

    def ruin_a_neighborhood(self, neighborhood_name):
        """
        Removes a neighborhood from the city.

        :param neighborhood_name: The name of the neighborhood that would be removed.
        """
        if neighborhood_name in self.neighborhoods:
            self.base_municipality_tax_rate *= 1.05
            self.neighborhoods.pop(neighborhood_name)
        else:
            raise KeyError(f"The neighborhood {neighborhood_name} doesnt exist in {self.city_name}")

    def build_a_neighborhood(self, neighborhood_name):
        """
        Adds a neighborhood to the city.

        :param neighborhood_name: The name of the neighborhood.
        :return A Neighborhood object if succeeded, None otherwise.
        """
        if neighborhood_name not in self.neighborhoods:
            self.base_municipality_tax_rate *= 1.1
            self.neighborhoods[neighborhood_name] = Neighborhood(neighborhood_name)
            return self.neighborhoods[neighborhood_name]
        else:
            print(f"The neighborhood {neighborhood_name} already exist in {self.city_name}")

    def build_a_house(self, neighborhood_name, number_of_family_members, size_of_house):
        """
        Adds a house to a neighborhood.

        :param neighborhood_name: The neighborhood that a house would be added to.
        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        if neighborhood_name in self.neighborhoods:
            self.neighborhoods[neighborhood_name].add_house(number_of_family_members, size_of_house)
        else:
            print(f"The neighborhood {neighborhood_name} doesnt exist in {self.city_name}")

    def build_a_park(self, neighborhood_name):
        """
        Adds a park to a neighborhood.

        :param neighborhood_name: The name of the neighborhood to which the park would be added.
        """
        if neighborhood_name in self.neighborhoods:
            self.neighborhoods[neighborhood_name].add_park()
        else:
            print(f"The neighborhood {neighborhood_name} doesnt exist in {self.city_name}")


class Neighborhood:
    """
    A neighborhood in Ackland (part of a City).
    """

    def __init__(self, name, number_of_parks=0, *houses):
        """
        Initiates a new Neighborhood object.

        :param name: The name of the neighborhood.
        :param number_of_parks: The number of parks in the neighborhood.
        :param houses: The number of houses in the neighborhood.
        """
        self.name = name
        self.number_of_parks = number_of_parks
        self.houses = list(houses)

    def get_neighborhood_tax_rate(self) -> int:
        """
        Calculates the amount of tax money that should be payed by the neighborhood, combining the amount payed by
        the neighborhood committee and each of the houses in the neighborhood.

        :return: The amount of money that should be payed by the neighborhood.
        """
        return self.base_neighborhood_tax_rate + sum([house.get_house_tax_rate() for house in self.houses])

    @property
    def base_neighborhood_tax_rate(self) -> int:
        """
        Calculates the amount of tax money that should be payed by the neighborhood committee.

        :return: The amount of money that should be payed by the committee.
        """
        return 5 * self.number_of_parks + 3 * len(self.houses)

    def build_house(self, number_of_family_members, size_of_house):
        """
        Adds a house to the neighborhood.

        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        self.houses.append(House(number_of_family_members, size_of_house))

    def build_park(self):
        """
        Adds a park to the neighborhood.
        """
        self.number_of_parks += 1


class House:
    """
    A house in Ackland (part of a Neighborhood).
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
    shenkler_city = City("shenklers_city")
    shenkler_neighborhood_1 = shenkler_city.build_a_neighborhood("Shenkler")
    shenkler_neighborhood_1.build_house(1, 1)
    shenkler_neighborhood_1.build_house(2, 1)
    shenkler_neighborhood_2 = shenkler_city.build_a_neighborhood("Shenkler2")
    shenkler_neighborhood_2.build_house(1, 1)
    shenkler_neighborhood_2.build_house(2, 1)
    print("Shenkler City tax rate (expected 1128):", shenkler_city.how_much_money())
    benor_city = City("benors_city")
    benor_neighborhood1 = benor_city.build_a_neighborhood("Benor")
    benor_neighborhood1.build_park()
    benor_neighborhood2 = benor_city.build_a_neighborhood("Benor2")
    benor_neighborhood2.build_park()
    print("Benor City tax rate (expected 1120)", benor_city.how_much_money())
    benor_city.ruin_a_neighborhood("Benor")
    print("Benor City tax rate after ruining Benor neighborhood (expected 1175)", benor_city.how_much_money())
    ackland = Ackland([shenkler_city, benor_city])
    print("Total tax in ackland: expected 2503.5", ackland.calculate_total_tax_amount())


if __name__ == "__main__":
    main()
