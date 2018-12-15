import time
import tensorflow
from .joueur import Joueur
from parser.read_question import Type
from parser.infos import current_turn_infos, game_over
from neuralnet.networks import CharacterChooseNetwork


class   Inspecteur(Joueur):
    def __init__(self):
        super().__init__(0)
        self.model = CharacterChooseNetwork()
        self.model.load()
        self.model = CharacterChooseNetwork()
        self.model.load()


    def lancer(self):
        while not self.game_over:
            self.init_turn()
            self.question.read()
            if self.question.type == Type.DRAW:
                if len(self.question.args) == 1:
                    self.act('0')
                infos, suspects = current_turn_infos(self.id)
                print(self.question.args)
                to_play = self.model.select_character(self.id, suspects, self.question.args)
                self.act(to_play)
            else:
                self.act('0')
            if game_over(self.id):
                self.game_over = True
