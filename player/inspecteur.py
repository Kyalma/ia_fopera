from .joueur import Joueur
from parser.infos import current_turn_infos

class   Inspecteur(Joueur):
    def __init__(self):
        Joueur.__init__(self, 0)

    def lancer(self):
        while not self.game_over:
            events, status = current_turn_infos(self.id)
            print(events)
            print(status)
            for suspect in status:
                self.suspects[suspect[:suspect.find('-')]].update(suspect)
