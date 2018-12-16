from .joueur import Joueur
from parser.read_question import Type
from parser.infos import current_turn_infos, game_over


class Inspecteur(Joueur):
    """
    IA de l'Inspecteur
    """
    def __init__(self):
        super().__init__(0)

    def lancer(self):
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
