import os
import json
import time

class   Logger():
    """
    Get data from the text files and output a JSON file
    at the end of game containing all the informations
    easy to read
    """
    def __init__(self, player_id: int):
        self.log_dir = './2'
        self._log = list()
        self.id = player_id
        self.current_turn = 0
        self._log.append(dict())

    def pass_turn(self):
        self.current_turn += 1
        self._log.append(dict())

    def log(self, **kwargs):
        self._log[self.current_turn].update(kwargs)

    def save(self):
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        with open(f'{self.log_dir}/gamelog-{self.id}-{int(time.time())}.json', 'w+') as fhandler:
            ret = json.dump(dict(turns=self._log), fhandler)
