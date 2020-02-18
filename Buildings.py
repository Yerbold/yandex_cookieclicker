import schedule


buildings = ['cursor', 'grandma', 'farm', 'mine', 'factory']

costs = {'cursor': 15,
         'grandma': 100,
         'farm': 1000,
         'mine': 12000,
         'factory': 130000
         }

productions = {'cursor': 0.1,
               'grandma': 1,
               'farm': 8,
               'mine': 47,
               'factory': 260
               }

# ---


class BuildingGroup:  # a group class that acts in the similar way of sprite.Group
    def __init__(self, cookie):
        self.group = []
        self.cookie = cookie
        self.total_production = 0

    def append(self, *building):
        self.group.extend(building)

    def buy_specific_building(self, index):
        if self.group[index].cost <= self.cookie.cookies_amount:
            self.cookie.add_cookies(-self.group[index].cost)
            self.group[index].buy()

    def get_building_cost(self, index):
        return self.group[index].cost

    def get_building_amount(self, index):
        return self.group[index].n

    def update_total_production(self):
        self.total_production = 0
        for index in range(1, len(self.group)):
            self.total_production += self.group[index].produce * self.group[index].n
            self.total_production = round(self.total_production, 2)

    def automatic_cookie_production(self):
        self.cookie.add_cookies(self.total_production * 0.1)


class Building:  # base class for every building
    def __init__(self, cost, produce):
        self.n = 0
        self.produce = produce
        self.cost = cost

    def buy(self):
        self.n += 1
        self.cost = int(self.cost * 1.3)


class Cursors(Building):  # cursor automatically clicks once every 10 seconds with 1 second delay between each other
    def __init__(self, cookie):
        super().__init__(costs['cursor'], productions['cursor'])
        self.latest_delay = 0
        self.cookie = cookie

    def buy(self):
        self.n += 1
        self.cost = int(self.cost * 1.2)
        schedule.every(10 + self.latest_delay).seconds.do(self.click)
        self.latest_delay += 1

    def click(self):
        self.cookie.add_cookies(self.cookie.cookies_per_click)


class Grandmas(Building):  # grandmas bake one cookie per second each
    def __init__(self):
        super().__init__(costs["grandma"], productions["grandma"])


class Farms(Building):  # farms produce 8 cookies per second each
    def __init__(self):
        super().__init__(costs['farm'], productions['farm'])


class Mines(Building):  # mines produce 47 cookies per second each
    def __init__(self):
        super().__init__(costs['mine'], productions['mine'])


class Factories(Building):  # factories produce 260 cookies per second each
    def __init__(self):
        super().__init__(costs['factory'], productions['factory'])
