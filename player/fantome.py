from .joueur import Joueur
from parser.infos import ghost_color

class   Fantome(Joueur):
    def __init__(self):
        Joueur.__init__(self, 1)
        self.color = None

    def lancer(self):
        while not self.game_over:
            self.color = ghost_color()
            print("Fantome debug: Je suis " + self.color)
