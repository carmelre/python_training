BASE_MUNICIPALITY_TAX_RATE = 1000


class City:
    """
    A City in Sim City.
    """
    def __init__(self, *neighborhoods):
        self.base_municipality_tax_rate = BASE_MUNICIPALITY_TAX_RATE
        self.neighborhoods = {neighborhood.name: neighborhood for neighborhood in neighborhoods}

    def how_much_money(self):
        return self.base_municipality_tax_rate + sum([neighborhood.get_neighborhood_tax_rate() for neighborhood
                                                     in self.neighborhoods.values()])

    def ruin_a_neighborhood(self):
        pass

    def build_a_neighborhood(self):
        pass


class Neighborhood:
    """
    A Neighborhood in Sim City (belongs to a City).
    """
    def __init__(self, name, number_of_parks=0, *houses):
        self.name = name
        self.number_of_parks = number_of_parks
        self.houses = houses

    def get_neighborhood_tax_rate(self):
        return self.base_neighborhood_tax_rate + sum([house.get_house_tax_rate for house in self.houses])

    @property
    def base_neighborhood_tax_rate(self):
        return 5*self.number_of_parks + 3*len(self.houses)


class House:
    """
    A House in Sim City (belongs to a Neighborhood).
    """
    def __init__(self, neighborhood_name, number_of_family_members, size_of_house):
        self.neighborhood_name = neighborhood_name
        self.number_of_family_members = number_of_family_members
        self.size_of_house = size_of_house

    def get_house_tax_rate(self)->int:
        return self.size_of_house * self.number_of_family_members
