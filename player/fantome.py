from .joueur import Joueur
from parser.infos import ghost_color

class   Fantome(Joueur):
    def __init__(self):
        Joueur.__init__(self, 1)
        self.color = None

    def lancer(self):
        self.color = ghost_color()
        pass
