import json
import numpy
from neuralnet.networks import CharacterChooseNetwork


def main():
    inputs_x = list()
    targets_y = list()
    with open('./data/training.json') as fhandler:
        data = json.load(fhandler)
        for row in data:
            inputs_x.append(numpy.array(row[0]))
            targets_y.append(numpy.array(row[1]))
    model = CharacterChooseNetwork()
    model.summary()
    model.train(numpy.array(inputs_x), targets_y)
    model.save()


if __name__ == "__main__":
    main()
