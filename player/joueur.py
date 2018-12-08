from game import characters
from parser.infos import current_turn_infos
from parser.read_question import Question

class   Joueur():
    def __init__(self, id):
        self.id = id
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

    def init_turn(self):
        events, status = current_turn_infos(self.id)
        for suspect in status:
            self.suspects[suspect[:suspect.find('-')]].update(suspect)
        pass


    def lancer(self):
        raise NotImplementedError()
