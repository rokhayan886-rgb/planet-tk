import random
import tkinter as tk
from S08_TP15 import *
import copy

class Turmite(Element):
    """Représente une fourmi de Langton sur la planète."""
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    def __init__(self, color):
        """
        Initialise une fourmi de Langton avec une couleur donnée.

        Args:
            color (str): Couleur de la fourmi.
        """
        super().__init__("\U0001F41C")
        self.__color = color
        self.__direction = Turmite.UP
        self.__position = None

    def get_color(self):
        return self.__color

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

class Turmites(PlanetTk):
    """Représente le jeu de Langton avec plusieurs fourmis sur une planète."""
    BACKGROUND_COLORS = ["#91797f", "#a8828c", "#a69096"]
    FOREGROUND_COLORS = named_colors = [
        "AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue",
        "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk",
        "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenrod", "DarkGray", "DarkGreen", "DarkKhaki", "DarkMagenta",
        "DarkOliveGreen", "DarkOrange", "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray",
        "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", "Firebrick", "FloralWhite",
        "ForestGreen", "Fuchsia", "Gainsboro", "GhostWhite", "Gold", "Goldenrod", "Gray", "Green", "GreenYellow", "Honeydew",
        "HotPink", "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon",
        "LightBlue", "LightCoral", "LightCyan", "LightGoldenrodYellow", "LightGray", "LightGreen", "LightPink", "LightSalmon",
        "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen",
        "Magenta", "Maroon", "MediumAquamarine", "MediumBlue", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue",
        "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin",
        "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenrod", "PaleGreen",
        "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "Red",
        "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue",
        "SlateBlue", "SlateGray", "Snow", "SpringGreen", "SteelBlue", "Tan", "Teal", "Thistle", "Tomato", "Turquoise", "Violet",
        "Wheat", "White", "WhiteSmoke", "Yellow", "YellowGreen"
    ]


    def __init__(self, lines_count, columns_count, cell_size = 30, speed = 100):
        """
         Initialise le jeu de Langton avec les paramètres spécifiés.

         Args:
             lines_count (int): Nombre de lignes de la planète.
             columns_count (int): Nombre de colonnes de la planète.
             cell_size (int): Taille des cellules de la planète (par défaut 30).
             speed (int): Vitesse de déplacement des fourmis (par défaut 100).
         """
        super().__init__(root=tk.Tk(), name ="Turmites", lattitude_cells_count= lines_count,  longitude_cells_count=columns_count, authorized_classes={Turmite},
                         cell_size = cell_size, gutter_size=0, background_color= self.BACKGROUND_COLORS)
        self.__lines_count = lines_count
        self.__columns_count = columns_count
        self.__is_playing = False
        self.__speed = speed

        canvas = self.get_canvas()

        for cell_number in range(self.__columns_count * self.__lines_count):
            self.set_cell_color(cell_number, self.BACKGROUND_COLORS)

            self.set_on_cell_click(cell_number, self.spawn_ant)
        canvas.bind("<space>", lambda event: self.change_simulation())
        canvas.bind("<Right>", lambda event : self.button_right())
        canvas.focus_set()

        canvas.pack()

        canvas.update()
        self.set_on_quit_click(self.quit)
        self.set_on_reset_click(self.reset)

    def change_simulation(self):
        """
        Change l'état de simulation (en cours ou arrêtée) et démarre ou arrête la boucle de simulation.
        """
        self.__is_playing = not self.__is_playing
        for cell in self.get_classes_cell_number()['Turmite']:
            self.repeat_movements(self.get_cell(cell))

    def repeat_movements(self,  ant: Turmite, event = None):
        """
        Répète les mouvements de la fourmi en continu lors de la simulation.

        Args:
            ant (Turmite): Instance de la fourmi.
            event (str, optional): Événement associé (par défaut None).
        """
        if self.__is_playing:
            self.move_ant(ant)
            self.get_canvas().after(self.__speed, lambda : self.repeat_movements(ant))

    def button_right(self):
        """
        Effectue une étape de simulation lors de l'appui sur la touche droite.
        """
        if not self.__is_playing:
            for cell in self.get_classes_cell_number()['Turmite']:
                self.move_ant(self.get_cell(cell))

    def move_ant(self, ant: Turmite):
        """
        Déplace une fourmi en fonction de sa couleur actuelle et met à jour la planète.

        Args:
            ant (Turmite): Instance de la fourmi à déplacer.
        """
        current_postion = copy.deepcopy(ant.get_position())
        next_position = self.next_position_of(ant)
        color = self.get_cell_color(current_postion)
        self.move_element(current_postion, next_position, self.get_cell_color(next_position))

        if color == ant.get_color():
            self.set_cell_color(current_postion, self.BACKGROUND_COLORS)
        else:
            self.set_cell_color(current_postion, ant.get_color())

    def next_position_of(self, ant : Turmite):
        """
        Calcule la prochaine position d'une fourmi en fonction de sa couleur et de sa direction actuelle.

        Args:
            ant (Turmite): Instance de la fourmi.

        Returns:
            int: Numéro de la cellule où la fourmi se déplacera.
        """
        direction = ant.get_direction()
        i, j = self.get_coordinates_from_cell_number(ant.get_position())
        color = self.get_cell_color(ant.get_position())
        if direction == Turmite.UP:
            if color == ant.get_color():
                ant.set_direction(Turmite.LEFT)
                j -= 1
            else:
                ant.set_direction(Turmite.RIGHT)
                j += 1

        elif direction == Turmite.DOWN:
            if color == ant.get_color():
                ant.set_direction(Turmite.RIGHT)
                j += 1
            else:
                ant.set_direction(Turmite.LEFT)
                j -= 1
        elif direction == Turmite.LEFT:
            if color == ant.get_color():
                ant.set_direction(Turmite.DOWN)
                i += 1
            else:
                ant.set_direction(Turmite.UP)
                i -= 1
        elif direction == Turmite.RIGHT:
            if color == ant.get_color():
                ant.set_direction(Turmite.UP)
                i -= 1
            else:
                ant.set_direction(Turmite.DOWN)
                i += 1


        i %= self.get_lines_count()
        j %= self.get_columns_count()
        ant.set_position(self.get_cell_number_from_coordinates(i, j))
        return self.get_cell_number_from_coordinates(i, j)

    def spawn_ant(self, cell_number):
        """
        Fait apparaître une nouvelle fourmi ou la supprime lors d'un clic sur une cellule.

        Args:
            event (str): Événement de clic.
            cell_number (int): Numéro de la cellule cliquée.
        """
        if isinstance(self.get_cell(cell_number), Turmite):
            self.die(cell_number)
        else:
            turmite = Turmite(random.choice(self.FOREGROUND_COLORS))
            turmite.set_position(cell_number)
            self.born(cell_number, turmite, turmite.get_color())

    def reset(self):
        """
        Réinitialise le jeu en remettant à zéro toutes les cellules et les fourmis.
        """
        for cell in range(self.__lines_count * self.__columns_count):
            self.__is_playing = False
            self.set_cell_color(cell, self.BACKGROUND_COLORS)
            if self.is_instance_of(cell, Turmite):
                self.die(cell)

if __name__ == "__main__":
    jeu = Turmites(25, 45, 20, speed = 10)
    jeu.start()