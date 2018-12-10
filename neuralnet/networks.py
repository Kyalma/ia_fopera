import datetime
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Activation, Flatten, MaxPooling2D, Dropout
from keras.optimizers import Adam, RMSprop



class   CharacterChooseNetwork():
    """
    Crée un modèle pour choisir un personnage à jouer en début de tour
    Le modèle reçoit en entrée une matrice numpy de taille (4, 3)
    Par exemple:
        [
            [4, 3, 0],       # 4 est la couleur du personnage traduite en chiffre (0 à 7)
            [2, 3, 1],       # 3 est la position du personnage sur le plateau
            [1, 2, 1],       # 1 est le status du personnage, 0 = suspect, 1 = innocenté
            [-1, -1, -1]     # -1 signifie qu'il n'y a pas de personnage à jouer
        ]
    Le modèle produit en output le score estimé en fin de tour pour avoir joué le personnage en question
    Par exemple:
        [0, 0, -1, 0]        # les valeurs des scores sont toujours négatives
    """
    def __init__(self):
        self.model = Sequential()
        self.model.add(
            Dense(4, input_shape=(4, 3), activation='relu'))                # Dense
        self.model.add(                                                     #  * relu
            Dense(8, activation='relu'))                                      # Dense
        self.model.add(                                                     #  * relu
            Flatten())                                                      # Flatten
        self.model.add(                                                     # Dense
            Dense(4, activation='softmax', init='random_uniform'))          #  * softmax
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    def load(self, name: str=None):
        if os.path.exists(name):
            self.model.load_weights(name)
            print("Loaded weights file successfully")
        else:
            print("Weight file '{}' not found".format(name))

    def save(self, end_time: datetime.datetime):
        self.model.save_weights("{}_{}it_{}.h5".format(
            self.weights_file_basename,
            self.iterations,
            end_time.strftime("%m%d%H%M%S")))

    def summary(self) -> None:
        self.model.summary()

model = CharacterChooseNetwork()
model.summary()
