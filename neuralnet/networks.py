import os
import time
import datetime
import numpy
import tensorflow

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Activation, Flatten, MaxPooling2D, Dropout, Conv1D
from keras.optimizers import Adam, RMSprop


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


class   CharacterChooseNetwork():
    """
    Crée un modèle pour choisir un personnage à jouer en début de tour
    Le modèle reçoit en entrée une matrice numpy de taille (4, 3)
    Par exemple:
        [
            [4, 3, 0],       # 4 est la couleur du personnage traduite en chiffre (0 à 7)
            [2, 3, 1],       # 3 est la position du personnage sur le plateau
            [5, 2, 1],       # 1 est le status du personnage, 0 = suspect, 1 = innocenté
            [-1, -1, -1]     # -1 signifie qu'il n'y a pas de personnage à jouer
        ]
    Le modèle produit en output le score estimé en fin de tour pour avoir joué le personnage en question
    Par exemple:
        [1, 2, 3, 0]        # les valeurs des scores sont inversées (car softmax > 0)
    """
    def __init__(self):
        self.graph = tensorflow.get_default_graph()
        self.model = Sequential()
        # self.model.add(
        #     Conv1D(8, input_shape=(8, 3) , kernel_size=(1, ), activation='relu'  ))
        self.model.add(
            Dense(8, input_shape=(8, 3), activation='relu'))                # Dense (* 8x3)
        self.model.add(                                                     #  * relu
            Dense(8, activation='relu'))                                    # Dense
        self.model.add(                                                     # Dropout 10%
            Dropout(0.1))
        self.model.add(                                                     #  * relu
            Dense(8, activation='relu'))                                    # Dense
        self.model.add(                                                     #  * relu
            Flatten())                                                      # Flatten
        self.model.add(                                                     # Dense
            Dense(8, activation='softmax', kernel_initializer='random_uniform'))          #  * softmax
        self.model.compile(loss='mse', optimizer='adam')

    def load(self, name: str='./data/player_select.h5'):
        if os.path.exists(name):
            self.model.load_weights(name)
            print("Loaded weights file successfully")
        else:
            print(f"Weight file '{name}' not found")

    def save(self):
        self.model.save_weights(f"data/player_select-{int(time.time())}.h5")

    def summary(self) -> None:
        self.model.summary()

    def train(self, input_x, target_y) -> None:
        prediction = self.model.predict(input_x)
        for i in range(0, prediction.shape[0]):
            index = numpy.argmax(target_y[i])
            prediction[i][index] = target_y[i][index]
        self.model.fit(input_x, prediction, epochs=32, verbose=0)

    def select_character(self, player_id: int, suspects: list, available: list) -> int:
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


# net = CharacterChooseNetwork()
# net.load()
# net.select_character(
#     0,
#     ['rose-1-suspect', 'gris-5-suspect', 'bleu-5-suspect', 'violet-3-suspect', 'marron-0-suspect', 'blanc-2-suspect', 'rouge-7-suspect', 'noir-5-suspect'],
#     ['gris-5-suspect', 'marron-0-suspect', 'bleu-5-suspect']
# )

