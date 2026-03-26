import tkinter as tk

from Conway import Conway
from SnakeGame import SnakeGame
from Turmites import Turmites
from S08_TP15 import PlanetTk
from S07_TP14_01 import Ground

class SuperPlanet(tk.Tk):
    BACKROUND_COLORS = ["#1215a6", "#0b0fe0", "#292bab", "#2d30c4"]
    HOVER = "#5557cf"

    def __init__(self, lines = 15, colonnes = 23):
        """
        Initialise la SuperPlanet avec une grille et des boutons pour les jeux.
        """
        super().__init__()
        self.__planetTk = PlanetTk(self, "Super Planet", longitude_cells_count=lines, lattitude_cells_count=colonnes, authorized_classes={Ground},
                            background_color= self.BACKROUND_COLORS, cell_size=25)
        self.__game_width = 40
        self.__game_height = 20
        self.__cell_size = 15

        canvas = self.__planetTk.get_canvas()

        for cell in range(lines * colonnes):
            self.__planetTk.set_cell_color(cell, self.BACKROUND_COLORS)
            canvas.tag_bind(f"c_{cell}", "<Enter>", lambda evt, c = cell: self.hover(c))
        WIDTH = 120
        HEIGHT = 30

        (tk.Button(self, text="Snake game", font="courier 10 bold", background="#dedede", activebackground="#1eb50b", activeforeground="white",
                   command= lambda : self.play_game(SnakeGame))
         .place(relx = 0.5, rely = 0.425, anchor = tk.CENTER, width= WIDTH, height = HEIGHT))

        (tk.Button(self, text="Conway", font="courier 10 bold", background="#dedede", activebackground="#1eb50b", activeforeground="white",
                   command= lambda : self.play_game(Conway))
         .place(relx = 0.5, rely = 0.5, anchor = tk.CENTER, width= WIDTH, height = HEIGHT))
        (tk.Button(self, text="Turmite", font="courier 10 bold", background="#dedede", activebackground="#1eb50b", activeforeground="white",
                   command= lambda : self.play_game(Turmites))
         .place(relx = 0.5, rely = 0.575, anchor = tk.CENTER, width= WIDTH, height = HEIGHT))

        self.resizable(False, False)
        canvas.pack()
        self.start_animation()

    def hover(self, cell):
        """
        Change la couleur de survol d'une cellule de la planète.

        Args:
            cell (int): Numéro de la cellule survolée.
        """
        self.__planetTk.set_cell_color(cell, self.HOVER)

    def start_animation(self):
        """Démarre une animation de fond sur la planète."""
        for i in range(5):
            self.__planetTk.born_randomly(Ground(), self.BACKROUND_COLORS)

        self.after(20, lambda : self.start_animation())
    def play_game(self, game):
        """
        Lance un jeu spécifié sur la SuperPlanète.

        Args:
            game (class): Classe du jeu à lancer.
        """
        self.destroy()
        game = game(self.__game_height, self.__game_width, self.__cell_size)
        game.start()

    def set_game_data(self, width = 40, height = 20, cell_size = 15):
        """
        Définit les données du jeu avec les valeurs spécifiées.

        Args:
            width (int): Largeur du jeu en nombre de cellules (par défaut 40).
            height (int): Hauteur du jeu en nombre de cellules (par défaut 20).
            cell_size (int): Taille des cellules du jeu en pixels (par défaut 15).
    """
        self.__cell_size = cell_size
        self.__game_width = width
        self.__game_height = height

    def open_window(self):
        """
        Ouvre la fenêtre principale du jeu.
        """
        self.mainloop()

if __name__ == "__main__":
    super_planet = SuperPlanet()
    super_planet.set_game_data(width=40, height=20, cell_size=15)
    super_planet.open_window()
