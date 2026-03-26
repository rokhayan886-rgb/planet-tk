from S07_TP14_01 import *
from S08_TP15 import PlanetTk
import tkinter as tk


class Wall(Element):
    def __init__(self):
        super().__init__("\U0001F9F1.")


class Fruit(Element):
    def __init__(self):
        super().__init__("\U0001F34E")
        self.__type = random.randint(0, 100)

    def get_points(self):
        type = self.__type
        if type < 5:
            return 5
        elif type < 25:
            return 2
        return 1


class Snake(Element):
    def __init__(self, min_speed=180, max_speed=100):
        Element.__init__(self, "\U0001F36B")
        self.__direction = 3
        self.__speed = min_speed
        self._max_speed = max_speed
        self.min_speed = min_speed
        self.__segments = []

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__speed

    def set_speed(self, speed):
        self.__speed = speed

    def get_max_speed(self):
        return self._max_speed

    def get_min_speed(self):
        return self.min_speed

    def get_segments(self):
        return self.__segments

    def set_segments(self, segments):
        self.__segments = segments

    def set_direction(self, direction):
        self.__direction = direction


class SnakeGame(PlanetTk):
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    THEMES = None

    BACKGROUND_COLORS = ["#2f1f8c", "#2b1b87", "#251778", "#21146b", "#2e1c97"]
    FOREGROUND_COLORS = ["#98a11f", "#939c19", "#8e9620", "#939c19"]
    WALL_COLORS = ["#235f7a"]
    HEAD_COLOR = "#777d29"
    FOOD_COLORS = ["pink", "green", "red", "yellow", "gold"]
    TEXT_COLOR = "white"

    direction_callback = True

    def __init__(self, lines_count, columns_count, max_speed=80, min_speed=180, cell_size=30, name = "Snake Game"):
        """
        Initialise le jeu du serpent avec les paramètres spécifiés.

        Args:
            lines_count (int): Nombre de lignes dans la grille du jeu.
            columns_count (int): Nombre de colonnes dans la grille du jeu.
            max_speed (int): Vitesse maximale du serpent (par défaut 80).
            min_speed (int): Vitesse minimale du serpent (par défaut 180).
            cell_size (int): Taille des cellules dans la grille du jeu (par défaut 30).
        """
        PlanetTk.__init__(self, tk.Tk(), name, authorized_classes={Snake, Fruit, Wall},
                          lattitude_cells_count=lines_count,
                          longitude_cells_count=columns_count, gutter_size=0, cell_size=cell_size,
                          background_color=self.BACKGROUND_COLORS,
                          foreground_color=self.FOREGROUND_COLORS)
        self.__lines_count = lines_count
        self.__columns_count = columns_count
        self.__snack = Snake(max(min_speed, max_speed), min(min_speed, max_speed))
        self.__theme = 0
        self.__is_playing = False
        self.__is_alive = False
        self.__walls = []
        self.__score = 0
        self.__snack.set_segments(self.random_snack_position())

        self.__game_over_label = None
        canvas = self.get_canvas()
        canvas.focus_set()
        self.set_on_space_click(self.change_simulation)
        self.import_themes()

        for i in range(lines_count):
            for j in range(columns_count):
                if j == 0 or j == columns_count - 1:
                    self.born(self.get_cell_number_from_coordinates(i, j), Wall(), self.WALL_COLORS)
                if i == 0 or i == lines_count - 1:
                    self.born(self.get_cell_number_from_coordinates(i, j), Wall(), self.WALL_COLORS)

        for cell_number in range(self.__columns_count * self.__lines_count):
            self.set_on_cell_click(cell_number, self.create_wall)
            if cell_number in self.__snack.get_segments():
                self.born(cell_number, Snake(), self.FOREGROUND_COLORS)
            elif not self.is_instance_of(cell_number, Wall):
                self.set_cell_color(cell_number, self.BACKGROUND_COLORS)
        tmp = {self.UP: "haut", self.DOWN: "bas", self.LEFT: "gauche", self.RIGHT: "droite"}
        canvas.create_text(35, 60, text=f"score : {self.__score}\n"
                                        f"speed : {self.__snack.get_speed()}\n"
                                        f"direction : {tmp[self.__snack.get_direction()]}\n"
                                        f"snake size : 3"
                                        f"", anchor="w", font="arial 10", fill=self.TEXT_COLOR, tags="info")

        self.get_canvas().pack()
        self.born_randomly(Fruit(), self.FOOD_COLORS)
        self.set_on_space_click(self.change_simulation)

        for button in ["<Up>", "<Down>", "<Left>", "<Right>"]:
            canvas.bind(button, self.change_direction)
        self.get_root().update()

        self.set_on_quit_click(self.quit)
        self.set_on_reset_click(self.reset)

    def change_simulation(self):
        """Change l'état de la simulation (en cours ou arrêtée) et démarre ou arrête la boucle de jeu."""
        self.__is_playing = not self.__is_playing
        self.loop()

    def loop(self):
        """Fait avancer le jeu en boucle en déplaçant le serpent."""
        if self.__is_playing:
            self.move_snack()
            self.direction_callback = True
            self.get_root().after(self.__snack.get_speed(), self.loop)

    def move_snack(self):
        """Déplace le serpent en fonction de sa direction actuelle et gère les collisions avec les murs et la nourriture."""
        segments = self.__snack.get_segments()
        self.set_cell_color(segments[0], self.FOREGROUND_COLORS)
        next_pos = self.get_next_cell_position()
        if self.is_instance_of(next_pos, Wall) or self.is_instance_of(next_pos, Snake):
            self.__is_playing = False
            self.__is_alive = False
            self.get_canvas().unbind("<space>")
            self.animate_death()
            self.__game_over_label = tk.Label(self.get_root(), text="Game Over!", font="courier 50 bold",
                                              background=random.choice(self.BACKGROUND_COLORS),
                                              foreground=random.choice(self.FOREGROUND_COLORS))
            self.__game_over_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

        segments.insert(0, next_pos)

        if self.is_instance_of(segments[0], Fruit):
            self.eat_food()
            self.born(segments[0], Snake())
            self.__snack.set_segments(segments)
        else:
            element = segments.pop()
            self.move_element(element, segments[0])
            self.set_cell_color(element, random.choice(self.BACKGROUND_COLORS))
        self.set_cell_color(segments[0], self.HEAD_COLOR)
        self.update_info()

    def change_direction(self, event):
        """Change la direction du serpent en fonction de la touche pressée."""
        if self.direction_callback:
            key = event.keysym
            direction = self.__snack.get_direction()
            keys = {"Up": 0, "Down": 1, "Left": 2, "Right": 3}

            if direction == self.UP and key != "Down":
                direction = keys[key]
            elif direction == self.DOWN and key != "Up":
                direction = keys[key]
            elif direction == self.LEFT and key != "Right":
                direction = keys[key]
            elif direction == self.RIGHT and key != "Left":
                direction = keys[key]
            self.__snack.set_direction(direction)
            self.direction_callback = False
        self.update_info()

    def get_next_cell_position(self):
        """Calcule la prochaine position du serpent en fonction de sa direction actuelle."""

        head_x, head_y = self.get_coordinates_from_cell_number(self.__snack.get_segments()[0])

        if self.__snack.get_direction() == self.UP:
            head_x -= 1
        elif self.__snack.get_direction() == self.DOWN:
            head_x += 1
        elif self.__snack.get_direction() == self.LEFT:
            head_y -= 1
        elif self.__snack.get_direction() == self.RIGHT:
            head_y += 1
        return self.get_cell_number_from_coordinates(head_x % self.__lines_count, head_y % self.__columns_count)

    def eat_food(self):
        """Fait manger au serpent le fruit et gère les effets de cette action (score, vitesse, etc.)."""
        self.born_randomly(Fruit(), self.FOOD_COLORS)
        self.__score += Fruit().get_points()
        if self.__snack.get_segments().__len__() % 5 == 0 and self.__snack.get_speed() > self.__snack.get_max_speed():
            self.__snack.set_speed(int(self.__snack.get_speed() * 0.9))

    def random_snack_position(self):
        """Génère aléatoirement une position pour le serpent lors du démarrage du jeu."""
        position = self.get_random_free_place()
        while not self.is_instance_of(position - 1, Ground) or not self.is_instance_of(position - 2, Ground):
            position = self.get_random_free_place()
        return [position, position - 1, position - 2]

    def animate_death(self):
        """Anime la mort du serpent en clinetont le corp de serpent."""

        if not self.__is_alive:
            snake = self.__snack.get_segments()
            if self.get_cell_color(snake[-1]) in self.FOREGROUND_COLORS:
                for cell in snake:
                    self.set_cell_color(cell, self.BACKGROUND_COLORS)
            else:
                for cell in snake:
                    self.set_cell_color(cell, self.FOREGROUND_COLORS)

            self.get_canvas().after(400, lambda: self.animate_death())

    def create_wall(self, cell_number):
        """Crée un mur à l'emplacement cliqué si aucun élément ne se trouve déjà là."""

        self.__walls.append(cell_number)
        if isinstance(self.get_cell(cell_number), Wall):
            self.die(cell_number)
        elif not isinstance(self.get_cell(cell_number), Fruit) \
                and not isinstance(self.get_cell(cell_number), Snake):
            self.born(cell_number, Wall(), self.WALL_COLORS)

    def update_info(self):
        """Met à jour les informations affichées à l'écran sur le score, la vitesse, la direction et la taille du serpent."""

        tmp = {self.UP: "haut", self.DOWN: "bas", self.LEFT: "gauche", self.RIGHT: "droite"}
        self.get_canvas().itemconfigure("info", text=f"score : {self.__score}\n"
                                                     f"speed : {self.__snack.get_speed()}\n"
                                                     f"direction : {tmp[self.__snack.get_direction()]}\n"
                                                     f"snake size : {len(self.__snack.get_segments())}"
                                        )

    def import_themes(self):
        """Importe les thèmes du fichier THEME.txt s'ils existent."""
        self.THEMES = []
        try:
            with open("THEMES.txt", "r") as file:
                theme = {}
                for line in file.readlines():
                    if line.startswith("#"):
                        self.THEMES.append(theme)
                        theme = {}
                    else:
                        key = line.split(" ")[0]
                        theme[key] = line.replace("\n", "").split(" ")[1:]
            self.get_canvas().bind("<c>", lambda evt: self.change_theme())
            for button in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                self.get_canvas().bind(f"{button}", lambda event, btn=button: self.change_theme(index=btn))
            self.__theme = random.randint(0, len(self.THEMES))
            self.change_theme(self.__theme)
        except FileNotFoundError:
            print("Le fichier THEME.txt n'existe pas !!!")
            self.THEMES = None

    def change_theme(self, index=-1):
        """Change le thème graphique du jeu en fonction de l'index spécifié ou en choisissant aléatoirement un thème."""

        if index != -1 and index < len(self.THEMES):
            self.__theme = index
        elif index >= len(self.THEMES):
            return
        else:
            self.__theme = (self.__theme + 1) % len(self.THEMES)

        self.BACKGROUND_COLORS = self.THEMES[self.__theme]["background"]
        self.FOREGROUND_COLORS = self.THEMES[self.__theme]["foreground"]
        self.WALL_COLORS = self.THEMES[self.__theme]["wall"]
        self.FOOD_COLORS = self.THEMES[self.__theme]["food"]
        self.HEAD_COLOR = self.THEMES[self.__theme]["head"]
        self.TEXT_COLOR = self.THEMES[self.__theme]["text"]
        tmp = {
            Wall: self.WALL_COLORS,
            Fruit: self.FOOD_COLORS,
            Snake: self.FOREGROUND_COLORS,
            Ground: self.BACKGROUND_COLORS
        }
        for cell in range(self.__lines_count * self.__columns_count):
            self.set_cell_color(cell, tmp[type(self.get_cell(cell))])
        self.set_cell_color(self.__snack.get_segments()[0], self.HEAD_COLOR)
        self.set_background_color(self.BACKGROUND_COLORS)
        self.set_foreground_color(self.FOREGROUND_COLORS)
        self.get_canvas().itemconfigure("info", fill=self.TEXT_COLOR)

        if self.__game_over_label is not None:
            self.__game_over_label.config(background=random.choice(self.BACKGROUND_COLORS),
                                          foreground=random.choice(self.FOREGROUND_COLORS))

    def reset(self):
        """Réinitialise le jeu, remettant à zéro le score, la vitesse et la position du serpent."""
        self.__score = 0
        self.__is_alive = True
        self.__is_playing = False
        for cell in self.__snack.get_segments():
            self.die(cell)

        self.__snack.set_segments(snack.random_snack_position())
        for cell in self.__snack.get_segments():
            self.born(cell, Snake())

        self.__snack.set_direction(SnakeGame.RIGHT)
        self.__snack.set_speed(self.__snack.get_min_speed())
        self.set_cell_color(self.__snack.get_segments()[0], self.HEAD_COLOR)
        self.set_on_space_click(self.change_simulation)

        if self.__game_over_label is not None:
            self.__game_over_label.destroy()
            self.__game_over_label = None
        self.update_info()


if __name__ == "__main__":
    snack = SnakeGame(30, 60, min_speed=150, max_speed=100, cell_size=15)
    snack.start()
