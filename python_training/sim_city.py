BASE_MUNICIPALITY_TAX_RATE = 1000


class City:
    """
    A city in Ackland.
    """
    def __init__(self, *neighborhoods):
        """
        Initiates a new City object.
        :param neighborhoods: A list of Neighborhood objects that represent the neighborhoods in the city.
        """
        self.base_municipality_tax_rate = BASE_MUNICIPALITY_TAX_RATE
        self.neighborhoods = {neighborhood.name: neighborhood for neighborhood in neighborhoods}

    def how_much_money(self)->int:
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

    def build_a_neighborhood(self, neighborhood_name, number_of_parks=0, *houses):
        """
        Adds a neighborhood to the city.
        :param neighborhood_name: The name of the neighborhood.
        :param number_of_parks: The number of parks in the neighborhood.
        :param houses: The number of houses in the neighborhood.
        """
        if neighborhood_name not in self.neighborhoods:
            self.base_municipality_tax_rate *= 1.1
            self.neighborhoods[neighborhood_name] = Neighborhood(neighborhood_name, number_of_parks, houses)

    def build_a_house(self, neighborhood_name, number_of_family_members, size_of_house):
        """
        Adds a house to a neighborhood.
        :param neighborhood_name: The neighborhood that a house would be added to.
        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        if neighborhood_name in self.neighborhoods:
            self.neighborhoods[neighborhood_name].add_house(House(neighborhood_name,
                                                                  number_of_family_members, size_of_house))

    def build_a_park(self, neighborhood_name):
        """
        Adds a park to a neighborhood.
        :param neighborhood_name: The name of the neighborhood to which the park would be added.
        """
        if neighborhood_name in self.neighborhoods:
            self.neighborhoods[neighborhood_name].add_park()


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

    def get_neighborhood_tax_rate(self)->int:
        """
        Calculates the amount of tax money that should be payed by the neighborhood, combining the amount payed by
        the neighborhood committee and each of the houses in the neighborhood.
        :return: The amount of money that should be payed by the neighborhood.
        """
        return self.base_neighborhood_tax_rate + sum([house.get_house_tax_rate for house in self.houses])

    @property
    def base_neighborhood_tax_rate(self)->int:
        """
        Calculates the amount of tax money that should be payed by the neighborhood committee.
        :return: The amount of money that should be payed by the committee.
        """
        return 5*self.number_of_parks + 3*len(self.houses)

    def add_house(self, house):
        """
        Adds a house to the neighborhood.
        :param house: A House object.
        """
        self.houses.append(house)

    def add_park(self):
        """
        Adds a park to the neighborhood.
        """
        self.number_of_parks += 1


class House:
    """
    A house in Ackland (part of a Neighborhood).
    """
    def __init__(self, neighborhood_name, number_of_family_members, size_of_house):
        """
        Initiates a new house object.
        :param neighborhood_name: The name of the neighborhood that the house belongs to.
        :param number_of_family_members: The number of family members in the house.
        :param size_of_house: The size of the house.
        """
        self.neighborhood_name = neighborhood_name
        self.number_of_family_members = number_of_family_members
        self.size_of_house = size_of_house

    def get_house_tax_rate(self)->int:
        """
        Calculates the amount of tax money that should be payed by the house.
        :return: The amount of money that should be payed by the house.
        """
        return self.size_of_house * self.number_of_family_members
