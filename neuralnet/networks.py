import os
import time
import datetime
import numpy

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
            Dense(8, activation='softmax', init='random_uniform'))          #  * softmax
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae', 'mse'])

    def load(self, name: str='./'):
        if os.path.exists(name):
            self.model.load_weights(name)
            print("Loaded weights file successfully")
        else:
            print("Weight file '{}' not found".format(name))

    def save(self):
        self.model.save_weights(f"data/player_select-{time.time()}.h5")

    def summary(self) -> None:
        self.model.summary()

    def train(self, input_x, target_y) -> None:
        prediction = self.model.predict(input_x)
        for i in range(0, prediction.shape[0]):
            index = numpy.argmax(target_y[i])
            prediction[i][index] = target_y[i][index]
        self.model.fit(input_x, prediction, epochs=32, verbose=0)
