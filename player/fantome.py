import time

from .joueur import Joueur
from parser.infos import ghost_color
from parser.read_question import Type

class   Fantome(Joueur):
    def __init__(self):
        super().__init__(1)
        self.color = None

    def lancer(self):
        self.color = ghost_color()
        print("Fantome debug: Je suis " + self.color)
        while not self.game_over:
            self.init_turn()
            self.question.read()
            if self.question.type == Type.DRAW:
                print(self.question.args)
                pass
            time.sleep(1)
