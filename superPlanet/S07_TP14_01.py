import random

class Element:
    def __init__(self, char_repr):
        self.__char_repr = char_repr

    def __repr__(self):
        return self.__char_repr

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__repr__() == other.__repr__()

class Ground(Element):
    def __init__(self):
        super().__init__('\u2B1C')

    def __repr__(self):
        return '\u2B1C'


class Resources(Element):
    def __init__(self, char_repr: str, value: float = 0):
        super().__init__(char_repr)
        self.__value = value

    def get_value(self):
        return self.__value

class Animal(Element):
    def __init__(self, char_repr, life_max):
        super().__init__(char_repr)
        self.__age = 0
        self.__gender = random.randint(0, 1)
        self.__bar_life = [life_max, life_max]
        self.__current_direction = []

    def get_age(self):
        return self.__age
    
    def ageing(self):
        self.__age += 1

    def get_gender(self):
        return self.__gender

    def get_life_max(self):
        return self.__bar_life[1]

    def get_life(self):
        pass

    def is_alive(self):
        return self.get_life() <= self.get_life_max()

    def is_dead(self):
        pass

    def recovering_life(self):
        pass

    def losing_life(self, value: int):
        pass

    def get_current_direction(self):
        return self.__current_direction

    def set_current_direction(self, line_direction: int, column_direction: int):
        self.__current_direction = [line_direction, column_direction]


class Water(Resources):
    def __init__(self):
        super().__init__('\U0001F41F')

class Herb(Resources):
    def __init__(self):
        super().__init__('\U0001F33F')

class Cow(Animal):
    def __init__(self):
        super().__init__('\U0001F42E', 1)

class Dragon(Animal):
    def __init__(self):
        super().__init__('\U0001F432', 1)

class Lion(Animal):
    def __init__(self):
        super().__init__('\U0001F981', 1)

class Mouse(Animal):
    def __init__(self):
        super().__init__('\U0001F42D', 1)


if __name__ == "__main__":
    print(Ground(), str(Ground()))
    print(Ground() == str(Ground()))
    print(Ground() == Ground())
    TYPES_COUNT = {Herb : 2, Water : 3, Cow : 2, Dragon : 1, Lion : 5, Mouse : 10}
    ELEMENT_BY_TYPE = {element_type : [element_type() for _ in range(element_count)]
                       for element_type, element_count in TYPES_COUNT.items()}
    for element_type, elements in ELEMENT_BY_TYPE.items():
        print(element_type.__name__, elements)