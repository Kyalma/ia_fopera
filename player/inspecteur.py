import time
from .joueur import Joueur
from parser.read_question import Type


class   Inspecteur(Joueur):
    def __init__(self):
        super().__init__(0)

    def lancer(self):
        while not self.game_over:
            self.init_turn()
            self.question.read()
            if self.question.type == Type.DRAW:
                print(self.question.args)
                pass
            time.sleep(1)
