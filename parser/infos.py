import re
import game.characters as characters



def ghost_color():
    with open('1/infos.txt', 'r') as fhandler:
        data = fhandler.readline()
    color = data.split()[-1]
    print(f"Le fantome est {color}")

def parse_events(events):
    tour = int(re.findall("Tour:([0-9]+),", events)[0])
    score = int(re.findall("Score:([0-9]+)/", events)[0])
    ombre = int(re.findall("Ombre:([0-9]),", events)[0])
    bloque = tuple(int(pos) for pos in re.findall("Bloque:{([0-9]), ([0-9])}", events)[0])
    return tour, score, ombre, bloque

def current_turn_infos(role):
    waiting = True
    while waiting:
        with open(f'{role}/infos.txt', 'r') as fhandler:
            data = fhandler.read()
        if data:
            waiting = False
        turns = data.split('**************************\n')
    if role == 0:
        turns.pop(0)
    current_turn = turns[-1].split('\n')
    events = parse_events(current_turn[0])
    status = current_turn[1].split()
    subs_current = turns[-1].split('****\n')
    subs_current.pop(0)
    for i, sub in enumerate(subs_current):
        for line in sub.split('\n'):
            if line.startswith("NOUVEAU PLACEMENT : "):
                new_pos = line[20:]
                for i, suspect in enumerate(status):
                    if suspect.startswith(new_pos[:new_pos.find('-')]):
                        status[i] = new_pos
            # Add new features here for parsing each turn
    return events, status
