import time

from .joueur import Joueur
from parser.infos import ghost_color, current_turn_infos, game_over
from parser.read_question import Type


class Fantome(Joueur):
    """
    IA du Fantôme
    """
    def __init__(self):
        super().__init__(1)
        self.color = None

    def lancer(self):
        self.color = ghost_color()
        print("Fantome debug: Je suis " + self.color)
        while not game_over(self.id):
            self.init_turn()
            self.question.read()
            if self.question.type == Type.DRAW:
                if len(self.question.args) == 1:
                    self.act('0')
                    continue
                infos, suspects = current_turn_infos(self.id)
                print(self.question.args)
                to_play = self.model.select_character(self.id, suspects,
                                                      self.question.args)
                self.act(to_play)
            else:
                self.random_act()
