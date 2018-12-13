from game import characters
from parser.infos import current_turn_infos
from parser.read_question import Question
from parser.logger import Logger

class   Joueur():
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

    def init_turn(self):
        events, positions = current_turn_infos(self.id)
        for suspect in positions:
            self.suspects[suspect[:suspect.find('-')]].update(suspect)
        self.logger.log(
            tour=events[0],
            score=events[1],
            ombre=events[2],
            bloqué=events[3],
            suspects=self.suspects
        )

    def lancer(self):
        raise NotImplementedError()
