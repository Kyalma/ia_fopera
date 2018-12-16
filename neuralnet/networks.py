import os
import time
import datetime
import numpy
import tensorflow

from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout


CHARACTER_VAL = {
    'marron': 0,
    'rose': 1,
    'noir': 2,
    'rouge': 3,
    'bleu': 4,
    'blanc': 5,
    'violet': 6,
    'gris': 7
}

STATUS_VAL = {
    'suspect': 0,
    'clean': 1
}


class BaseNetwork():
    def __init__(self, weight_file: str):
        self.weight_file = weight_file
        self.graph = tensorflow.get_default_graph()
        self.model = Sequential()

    def summary(self) -> None:
        self.model.summary()

    def load(self):
        if os.path.exists(self.weight_file):
            self.model.load_weights(self.weight_file)
            print("Loaded weights file successfully")
        else:
            print(f"Weight file '{self.weight_file}' not found")

    def save(self):
        self.model.save_weights(self.weight_file)


class CharacterChooseNetwork(BaseNetwork):
    """
    Crée un modèle pour choisir un personnage à jouer en début de tour
    Le modèle reçoit en entrée une matrice numpy de taille (8, 3) comprenant
    la liste de tout les personnages
    Par exemple:
        [
            [<couleur>, <position>, <status>],
            ...
        ]
    La couleur du personnage est traduite en chiffre, ainsi que son status
    suspect ou innocenté
    Le modèle produit en sortie la 'la probabilité' de produire un score élevé
    pour chaque personnage
    Par exemple:
        [0.11, 0.10, 0.24, 0.03, ...]
    """
    def __init__(self):
        super().__init__('data/player_select.h5')
        self.model.add(
            Dense(8, input_shape=(8, 3), activation='relu'))    # Dense (* 8x3)
        self.model.add(                                         # * relu
            Dense(8, activation='relu'))                        # Dense
        self.model.add(                                         # Dropout 10%
            Dropout(0.1))
        self.model.add(                                         # * relu
            Dense(8, activation='relu'))                        # Dense
        self.model.add(                                         # * relu
            Flatten())                                          # Flatten
        self.model.add(                                         # Dense
            Dense(8, activation='softmax',                      # * softmax
                  kernel_initializer='random_uniform'))
        self.model.compile(loss='mse', optimizer='adam')

    def train(self, input_x, target_y) -> None:
        prediction = self.model.predict(input_x)
        for i in range(0, prediction.shape[0]):
            index = numpy.argmax(target_y[i])
            prediction[i][index] = target_y[i][index]
        self.model.fit(input_x, prediction, epochs=32, verbose=1)

    def select_character(self, player_id: int, suspects: list,
                         available: list) -> int:
        """
        Predict which character is the best to use for each player
        """
        tmp_x = list()
        for character in suspects:
            color, pos, status = character.split('-')
            tmp_x.append([CHARACTER_VAL[color], int(pos), STATUS_VAL[status]])
        input_x = numpy.expand_dims(
            numpy.array(sorted(tmp_x, key=lambda suspect: suspect[0])),
            axis=0)
        with self.graph.as_default():
            prediction = self.model.predict(input_x)[0]
        possibilities = list()  # type: list
        for character in available:
            color, __, __ = character.split('-')
            possibilities.append(prediction[CHARACTER_VAL[color]])
        if player_id == 1:  # Si on jour le fantome, on veut gagner des points
            best = numpy.argmax(possibilities)
        else:
            best = numpy.argmin(possibilities)
        return best
