import random

from game import characters
from parser.infos import current_turn_infos
from parser.read_question import Question
from parser.logger import Logger
from neuralnet.networks import CharacterChooseNetwork

random.seed()


class Joueur():
    """
    Classe abstraite pour la création d'une IA de joueur
    """
    def __init__(self, player_id: int):
        self.id = player_id
        self.suspects = {
            'marron': characters.Brown(),
            'rose': characters.Pink(),
            'noir': characters.Black(),
            'rouge': characters.Red(),
            'bleu': characters.Blue(),
            'blanc': characters.White(),
            'violet': characters.Violet(),
            'gris': characters.Grey()
        }
        self.question = Question(f'{self.id}/questions.txt')
        self.game_over = False
        self.logger = Logger(self.id)
        self.model = CharacterChooseNetwork()
        self.model.load()

    def init_turn(self):
        events, positions = current_turn_infos(self.id)
        for suspect in positions:
            self.suspects[suspect[:suspect.find('-')]].update(suspect)

    def lancer(self):
        raise NotImplementedError()

    def act(self, answer):
        with open(f'{self.id}/reponses.txt', 'w') as fhandler:
            fhandler.write(str(answer))

    def random_act(self):
        self.act(random.randint(0, len(self.question.args) - 1))
