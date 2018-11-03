import re
from time import sleep

import game.characters as characters

def read_file(file, wait=True, readline=False) -> str:
    while wait:
        with open(file, 'r') as fhandler:
            if readline:
                data = fhandler.readline()
            else:
                data = fhandler.read()
        if data:
            wait = False
        sleep(0.1)
    return data

def ghost_color() -> str:
    data = read_file('1/infos.txt', readline=True)
    color = data.split()[-1]
    return color

def parse_events(events) -> tuple:
    tour = int(re.findall("Tour:([0-9]+),", events)[0])
    score = int(re.findall("Score:([0-9]+)/", events)[0])
    ombre = int(re.findall("Ombre:([0-9]),", events)[0])
    bloque = tuple(int(pos) for pos in re.findall("Bloque:{([0-9]), ([0-9])}", events)[0])
    return tour, score, ombre, bloque

def current_turn_infos(role):
    data = read_file(f'{role}/infos.txt')
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
