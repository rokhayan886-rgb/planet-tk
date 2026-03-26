import random
from S05_TP09_01_template import Grid

class PlanetAlpha(Grid):
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    def __init__(self, name : str, latitude_cells_count : int, longitude_cells_count: int, ground):
        Grid.__init__(self, [[ground] * longitude_cells_count for _ in range(latitude_cells_count)])
        self.__name = name
        self.__ground = ground

    def get_name(self): return self.__name

    def get_ground(self): return self.__ground

    def has_ground(self):
        grid = self.get_grid()
        for row in grid:
            if self.get_ground() in row:
                return True
        return False

    def get_random_free_place(self):
        grid_size = self.get_lines_count() * self.get_columns_count()

        while True:
            random_num = random.randint(0, grid_size - 1)
            if type(self.get_cell(random_num)) == type(self.get_ground()):
                return random_num

    def born(self, cell_number : int, element):
        self.set_cell(cell_number, element)

    def die(self, cell_number : int):
        self.set_cell(cell_number, self.get_ground())

    def __repr__(self):
        grid = ""
        for line in self.get_grid():
            for element in line:
                grid += str(element)
            grid += '\n'

        habitants = sum([1 for element in grid.replace('\n', "") if str(element) != str(self.get_ground())])

        return f"{self.get_name()} ({habitants} habitants)\n{grid}"


if __name__ == "__main__":
    PLANET_TEST = PlanetAlpha("Terre", 5, 10, '.')
    INHABITANTS_TEST = {'D': 7, 'C': 3}
    RESOURCES_TEST = {'E': 10, 'H': 20}
    print(PLANET_TEST)

    for letter , letter_count in INHABITANTS_TEST.items():
        for _ in range(letter_count):
            PLANET_TEST.born(PLANET_TEST.get_random_free_place(), letter)
    print(PLANET_TEST)

    for letter , letter_count in RESOURCES_TEST.items():
        for _ in range(letter_count):
            PLANET_TEST.born(PLANET_TEST.get_random_free_place(), letter)
    print(PLANET_TEST)

    print(PLANET_TEST.get_neighbour(0, 0, PlanetAlpha.NORTH_WEST))
    print(PLANET_TEST.get_neighborhood(0, 0, PlanetAlpha.WIND_ROSE))
    PLANET_TEST.die(0)

    for cell in PLANET_TEST.get_cell_neighborhood_numbers(0, PLANET_TEST.WIND_ROSE):
        PLANET_TEST.die(cell)
    print(PLANET_TEST)
    print(PLANET_TEST.get_neighborhood(0, 0, PlanetAlpha.WIND_ROSE))
