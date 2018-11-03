import os
from time import sleep
from enum import Enum

class TYPE(Enum):
    POWER = 0
    DRAW = 1
    POSITION = 2
    PURPLE_POWER = 3
    GRAY_POWER = 4
    BLUE_POWER = 5
    BLUE_POWER_EXIT = 6
class Question:
    def __init__(self, file):
        self.file = file
        self.type = None
        self.args = None
        self.isEmpty = False
    def read(self, wait=True):
        while os.stat(self.file).st_size == 0:
            self.isEmpty = True
            if not wait:
                return
            sleep(0.01)
        self.isEmpty = False
        with open(self.file, 'r') as filehandler:
            data = filehandler.read()
        qdata = data.split()
        if qdata[0] == 'Voulez-vous':
            print('0')
            self.type = TYPE.POWER
        elif qdata[0] == 'positions':
            self.type = TYPE.POSITION
            self.args = data[data.find('{')+1:data.find('}')].split(', ') 
        elif qdata[0] == 'Tuiles':
            self.type = TYPE.DRAW
            self.args = data[data.find('[')+1:data.find(']')].split(', ')        
        elif qdata[0] == 'Quelle' and qdata[1] == 'salle' and qdata[2] == 'bloquer':
            self.type = TYPE.BLUE_POWER
            self.args = data[data.find('{')+1:data.find('}')].split(', ')
        elif qdata[0] == 'Quelle' and qdata[1] == 'sortie':
            self.type = TYPE.BLUE_POWER_EXIT
        elif qdata[0] == 'Quelle' and qdata[1] == 'salle' and qdata[2] == 'obscurcir':
            self.type = TYPE.GRAY_POWER
        else:
            self.type = TYPE.PURPLE_POWER
        with open(self.file, 'w') as filehandler:
            filehandler.seek(0)
            filehandler.truncate()
if __name__=="__main__":
    question = Question('../0/questions.txt')
    question.read()
    print(question.type)
    print(question.args)
    print(question.isEmpty)
