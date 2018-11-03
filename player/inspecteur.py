from .joueur import Joueur
from parser.infos import current_turn_infos
from parser.read_question import TYPE

class   Inspecteur(Joueur):
    def __init__(self):
        Joueur.__init__(self, 0)

    def lancer(self):
        while not self.game_over:
            events, status = current_turn_infos(self.id)
            for suspect in status:
                self.suspects[suspect[:suspect.find('-')]].update(suspect)
            self.question.read()
            if self.question.type == TYPE.DRAW:
                print(self.question.args)
                pass
            sleep(1)
