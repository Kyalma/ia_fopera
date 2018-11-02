import game.characters as characters

suspects = {
    'marron': characters.Brown(),
    'rose': characters.Pink(),
    'noir': characters.Black(),
    'rouge': characters.Red(),
    'bleu': characters.Blue(),
    'blanc': characters.White(),
    'violet': characters.Violet(),
    'gris': characters.Grey()
}

def pawns_position():
    pass

def ghost_color():
    with open('../0/infos.txt', 'r') as fhandler:
        data = fhandler.readline()
    *__ , color = data.split()
    print(f"Le fantome est {color}")

def current_turn_infos(role):
    with open(f'{role}/infos.txt', 'r') as fhandler:
        turns = fhandler.read().split('**************************\n')
        if role == 0:
            turns.pop(0)
        current_turn = turns[-1].split('\n')
        events = current_turn[0]
        status = current_turn[1].split()
        return events, status


if __name__ == "__main__":
    events, status = current_turn_infos(0)
    for suspect in status:
        suspects[suspect[:suspect.find('-')]].update(suspect)
    for color in suspects:
        print(suspects[color], end='\n')

