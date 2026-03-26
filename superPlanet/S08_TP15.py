import tkinter as tk
from S06_TP11 import PlanetAlpha
from S07_TP14_01 import *

class PlanetTk(PlanetAlpha):
    def __init__(self, root: tk.Tk, name: str, lattitude_cells_count:int, longitude_cells_count:int,
                 authorized_classes, background_color='white', foreground_color='dark blue',
                 gridlines_color:str="maroon", cell_size = 40, gutter_size =  0, margin_size = 0,
                 show_content:bool= True, show_grid_lines = True, **kw):
        PlanetAlpha.__init__(self, name, lattitude_cells_count, longitude_cells_count, Ground())
        root.title(name)
        kw["width"] = longitude_cells_count * cell_size + (longitude_cells_count - 1) * gutter_size + 2 * margin_size
        kw["height"] = lattitude_cells_count * cell_size + (lattitude_cells_count - 1) * gutter_size + 2 * margin_size

        self.__cell_size = cell_size
        self.__gutter_size = gutter_size
        self.__margin_size = margin_size
        self.__root = root

        self.__canvas = tk.Canvas(root, width=kw["width"], height=kw["height"])

        self.__show_content = show_content
        self.show_grid_lines = show_grid_lines
        self.__authorized_classes = authorized_classes
        self.__background_color = background_color
        self.__foreground_color = foreground_color
        self.__gridlines_color = gridlines_color

        for cell_number in range(lattitude_cells_count * longitude_cells_count):
            i, j = self.get_coordinates_from_cell_number(cell_number)

            x = margin_size + j * (cell_size + gutter_size)
            y = margin_size + i * (cell_size + gutter_size)

            self.__canvas.create_rectangle(x, y, x + cell_size, y + cell_size, tags=(f'c_{cell_number}',), outline="")



        self.images = [tk.PhotoImage(file="ICONS/exit.png"), tk.PhotoImage(file="ICONS/reset.png")]


    def set_on_space_click(self, function):
        self.__canvas.bind("<space>", lambda  evt : function())

    def set_on_cell_click(self, cell_number, function):
        self.__canvas.tag_bind(f"c_{cell_number}", "<Button-1>", lambda event, cel = cell_number : function(cel))

    def set_on_quit_click(self, function):
        self.__canvas.create_image(self.get_root().winfo_width() - 60, 50, image= self.images[0], tags="quitter")
        self.__canvas.tag_bind("quitter", "<Button-1>", lambda e : quit())

    def set_on_reset_click(self, function):
        self.__canvas.create_image(self.get_root().winfo_width() - 110, 50, image= self.images[1], tags= "reset")
        self.__canvas.tag_bind("reset", "<Button-1>", lambda e : function())

    def is_instance_of(self, cell_number, type):
        return isinstance(self.get_cell(cell_number), type)

    def get_canvas(self):
        return self.__canvas

    def get_root(self):
        return self.__root

    def get_cell_size(self):
        return self.__cell_size

    def start(self):
        self.__root.mainloop()

    def get_gutter_size(self):
        return self.__gutter_size


    def get_margin_size(self):
        return self.__margin_size

    def get_background_color(self):
        return self.__background_color

    def set_background_color(self, color):
        self.__background_color = color

    def get_foreground_color(self):
        return self.__foreground_color

    def set_foreground_color(self, color):
        self.__foreground_color = color

    def born(self, cell_number : int, element, color = None): #ajoute des elements dans la grille
        super().born(cell_number, element)

        if color is None:
            color = self.get_foreground_color()

        self.set_cell_color(cell_number, color)

    def die(self, cell_number : int):
        super().die(cell_number)
        self.set_cell_color(cell_number, self.get_background_color())

    def set_cell_color(self, cell_number, cell_color):
        if isinstance(cell_color, str):
            self.__canvas.itemconfigure(f'c_{cell_number}', fill = cell_color)
        else:
            self.__canvas.itemconfigure(f'c_{cell_number}', fill = random.choice(cell_color))


    def get_cell_color(self, cell_number):
        return self.__canvas.itemcget(f"c_{cell_number}", 'fill')

    def born_randomly(self, element, color=None):
        if color == None:
            color = self.__foreground_color

        if not element.__class__ in self.__authorized_classes:
            raise TypeError(f"Type of ({element.__class__}) is not allowed")

        if self.has_ground():
            self.born(self.get_random_free_place(), element, color)

    def populate(self, class_names_count):
        for element_type, element_count in class_names_count.items():
            for _ in range(element_count):
                self.born_randomly(element_type())


    def move_element(self, cell_number, new_cell_number, color=None):
        self.born(new_cell_number, self.get_cell(cell_number), color)
        self.die(cell_number)


    def get_classes_cell_number(self):
        classes_cell_numbers = {}
        for type in self.__authorized_classes:
            cells = []
            for cell_number in range(self.get_columns_count() * self.get_lines_count() - 1):
                if not isinstance(self.get_cell(cell_number), Ground) and isinstance(self.get_cell(cell_number), type):
                    cells.append(cell_number)
            classes_cell_numbers[type.__name__] = cells
        return classes_cell_numbers

    def quit(self):
        self.get_root().quit()
        self.get_root().destroy()


if __name__ == "__main__":
    random.seed(1)
    PLANET_NAME = "EARTH"
    COLUMNS_COUNT = 12
    LINES_COUNT = 12
    AUTHORIZED_CLASSES = {Ground, Water, Herb, Lion, Dragon, Cow, Mouse}
    CELL_SIZE = 50
    TYPES_COUNT = {Herb : 2, Water : 3, Cow : 2, Dragon : 1, Lion : 5, Mouse : 10}


    planet = PlanetTk(tk.Tk(), PLANET_NAME, COLUMNS_COUNT, LINES_COUNT, AUTHORIZED_CLASSES,
                      cell_size= CELL_SIZE, show_content=False)
    planet.populate(TYPES_COUNT)
    print(planet)
    planet.move_element(0, 12)
    print(planet)





