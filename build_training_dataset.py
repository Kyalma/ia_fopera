import os
import json
from neuralnet.networks import CHARACTER_VAL, STATUS_VAL

LOG_DATA_DIR = './log'
OUTPUT_DIR = './data'


def main():
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    training_dataset = list()
    for filepath in os.listdir(LOG_DATA_DIR):
        if not filepath.startswith('gamelog'):
            continue
        with open(f"{LOG_DATA_DIR}/{filepath}", 'r') as fhandler:
            data = json.load(fhandler)
            for turn in data['turns']:
                target_y = [0] * 8
                score_target = turn['score fin'] - turn['score']
                perso_target, __, __ = turn['perso joué'].split('-')
                target_y[CHARACTER_VAL[perso_target]] = score_target
                input_x = list()
                for character in turn['suspects']:
                    color, pos, status = character.split('-')
                    input_x.append([CHARACTER_VAL[color], int(pos), STATUS_VAL[status]])
                input_x = sorted(input_x, key=lambda suspect: suspect[0])
                training_dataset.append([input_x, target_y])
    with open(f"{OUTPUT_DIR}/training.json", 'w') as fhandler:
        json.dump(training_dataset, fhandler)

if __name__ == "__main__":
    main()
