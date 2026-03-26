from S08_TP15 import *
import copy as cp

class Human(Element):

    def __init__(self):
        super().__init__("\U0001F9D1")

class Conway(PlanetTk):

    BACKGROUND_COLORS = ["#fffdd4", "#f5f3c4", "#fffdd9", "#f7f5c1"]
    FOREGROUND_COLORS = ["#42420a"] #clrs des humains

    def __init__(self, lines_count, columns_count, name="Conway", cell_size = 30):
        """
        Initialise le jeu de la vie de Conway avec les paramètres spécifiés.

        Args:
            lines_count (int): Nombre de lignes de la planète.
            columns_count (int): Nombre de colonnes de la planète.
            cell_size (int): Taille des cellules de la planète (par défaut 30).
            name (str): Nom du jeu (par défaut "Conway").
        """
        super().__init__(root= tk.Tk(), name =name, authorized_classes = {Human}, lattitude_cells_count=lines_count,
                         longitude_cells_count=columns_count, cell_size= cell_size, background_color=self.BACKGROUND_COLORS,
                         foreground_color=self.FOREGROUND_COLORS)
        self.__lines_count = lines_count
        self.__columns_count = columns_count
        self.__generation_count = 0
        self.__simulation_on = False

        canvas = self.get_canvas()
        #get_canvas est une fonction tp15 qui renvoie le canvas
        # Création de chaque case de la grille en fonction de __columns_count et __lines_count
        for cell_number in range(self.__columns_count * self.__lines_count):#parcours la grille
            self.set_cell_color(cell_number, self.BACKGROUND_COLORS) # la fonction set_cell_color change la couleurs de cellule en fonction du numero de cellule
            self.set_on_cell_click(cell_number, self.invert_cell)  # la fonction set_on_cell_click inverse la cellule en fonction du numero de cellule quand on click
        # cell_number represente le nbre d'une cellule
        self.__info_label = tk.Label(self.get_root(), text="Generation : 0\nPopulation : 0", justify="left", font="courier 12 bold", background=random.choice(self.BACKGROUND_COLORS), foreground=random.choice(self.FOREGROUND_COLORS))# represente l'infos (g2eneretion population)
        self.__info_label.place(relx = 0.02, rely = 0.02) # l'emplacement de label
        canvas.focus_set() # capte le click du clavier
        self.set_on_space_click(self.change_simultation) # appel la fonction change_simultation quand on click
        canvas.bind("<Right>", self.etape_suivant) # appel la fonctione tape_suivant quand on click l'orsque la bouton droite est clic
        self.get_canvas().pack()  #la meme chose que place
        self.get_canvas().update() # mettre a jour les longueur et largeur de cellule
        self.set_on_quit_click(self.quit) # quand on appuie sur le bouton clicker et pour ajouter l'image
        self.set_on_reset_click(self.reset) # le bouton initialiser est clicker et pour ajouter l'image

    def change_simultation(self):
        """
        Change l'état de simulation (en cours ou arrêtée) et démarre ou arrête la boucle de simulation.
        """
        self.__simulation_on = not self.__simulation_on
        self.start_simualation()

    def start_simualation(self, event = None):
        """
        Boucle de simulation pour mettre à jour automatiquement le jeu.

        Args:
            event (str, optional): Événement de boucle de simulation (par défaut None).
        """
        if self.__simulation_on == True:
            self.etape_suivant()
            self.get_canvas().after(70, self.start_simualation) # reappelle la fonction apres 70millisesonde 70 est la vitesse de jeux

    def etape_suivant(self, event = None):
        """
        Effectue une étape dans le jeu, mettant à jour la génération et l'état des cellules. change les etapes

        Args:
            event (str, optional): Événement déclencheur (par défaut None).
        """
        if event != None and event.keysym == "Right" and self.__simulation_on:# verifier si le boutton right est clicker et que le jeu est entrain de jouer  il return rien
            return

        self.__generation_count += 1
        grille = cp.deepcopy(self.get_grid()) # donne une copie de la grille

        for cell_number in range(self.get_columns_count() * self.get_lines_count()):
            nb_voisins = self.get_living_neighbors_number(grille, cell_number=cell_number)#Renvoie le nombre de voisins vivants d'une cellule donnée dans la grille.pour rendre chaque cellule independanr
            i, j = self.get_coordinates_from_cell_number(cell_number) #convertis en numero de cellule
            if isinstance(grille[i][j], Human):
                if nb_voisins > 3 or nb_voisins < 2:
                    self.die(cell_number)
                    self.set_cell_color(cell_number, random.choice(self.BACKGROUND_COLORS))
            else:
                if nb_voisins == 3:
                    self.born(cell_number, Human())
        self.__info_label.configure(text = f"Generation : {self.__generation_count}\nPopulation : {self.get_living_count()}")# la fonction get_living_count() Renvoie le nombre d'êtres humains vivants sur la planète
        print(self)

    def get_living_neighbors_number(self, grille, cell_number, isTore = True):
        """
            Renvoie le nombre de voisins vivants d'une cellule donnée dans la grille.

            Args:
                grille (list): Grille de la planète.
                cell_number (int): Numéro de la cellule à vérifier.
                isTore (bool, optional): Indique si la grille est considérée comme un tore (par défaut True).

            Returns:
                int: Nombre de voisins vivants de la cellule.
            """
        voisins = self.get_cell_neighborhood_numbers(cell_number, self.WIND_ROSE, isTore)# renvoie les position de ses voisins
        counter = 0
        for voisin in voisins:
            i, j = self.get_coordinates_from_cell_number(voisin)
            if isinstance(grille[i][j], Human):
                counter += 1
        return counter

    def get_living_count(self): #utiliser pour afficher le nbre de polution
        """
        Renvoie le nombre d'êtres humains vivants sur la planète.

        Returns:
            int: Nombre d'êtres humains vivants.
        """
        count = 0
        for cell_number in range(self.__lines_count * self.__columns_count):
            if isinstance(self.get_cell(cell_number), Human):
                count += 1
        return count


    def invert_cell(self, cell_number):
        """
        Inverse l'état d'une cellule (humaine ou vide) lors d'un clic.

        Args:
            cell_number (int): Numéro de la cellule à inverser.
        """
        if isinstance(self.get_cell(cell_number), Human): # verifie si le type est human ou pas si oui il le tue et change sa colr de fond inversement
            self.die(cell_number)
            self.set_cell_color(cell_number, self.BACKGROUND_COLORS)
        else:
            self.born(cell_number, Human(), self.FOREGROUND_COLORS) #la foncion self.born change l'element dont la position est cell_number dans la grille
        self.__info_label.configure(text = f"Generation : {self.__generation_count}\nPopulation : {self.get_living_count()}")# la fonction  modifier le texte
    def reset(self):
        """
        Réinitialise le jeu, remettant à zéro toutes les cellules.
        Args:
            event (str, optional): Événement de réinitialisation (par défaut None).
        """
        for cell in range(self.__lines_count * self.__columns_count):
            if self.is_instance_of(cell, Human):
                self.die(cell)
        self.__generation_count = 0
        self.__simulation_on = False
        self.__info_label.configure(text = f"Generation : {self.__generation_count}\nPopulation : {self.get_living_count()}")

if __name__ == "__main__":
    jeu_1 = Conway(25, 40, cell_size=25)
    jeu_1.start()




