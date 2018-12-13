import os
import json

RAW_DATA_DIR = './2'
OUTPUT_DIR = './data'

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

def main():
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    training_dataset = list()
    for filepath in os.listdir(RAW_DATA_DIR):
        if not filepath.startswith('gamelog'):
            continue
        with open(f"{RAW_DATA_DIR}/{filepath}", 'r') as fhandler:
            data = json.load(fhandler)
            for turn in data['turns']:
                if not turn:
                    continue
                target = turn['score fin'] - turn['score']
                for character in turn['suspects']:
                    color, pos, status = character.split('-')
                input_x = [CHARACTER_VAL[color], int(pos), STATUS_VAL[status]]
                training_dataset.append([input_x, target])
    with open(f"{OUTPUT_DIR}/training.json", 'w') as fhandler:
        json.dump(training_dataset, fhandler)

if __name__ == "__main__":
    main()
