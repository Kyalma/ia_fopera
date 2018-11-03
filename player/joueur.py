from game import characters
from parser import 

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

    def lancer(self):
        raise NotImplementedError()
