import re
from time import sleep
from parser.read_question import Question, Type

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

def all_turns(role: int) -> list:
    all_turns_info = list()
    question = Question(None)
    data = read_file(f'{role}/infos.txt')
    turns = data.split('**************************\n')
    turns.pop(0)
    for big_turn in turns:
        turn_meta = big_turn.split('\n', 2)
        big_events = parse_events(turn_meta[0])
        suspects = turn_meta[1].split()
        sub_turns = big_turn.split('****\n')
        sub_turns.pop(0)
        for sub_turn in sub_turns:
            turn_info = dict()
            turn_info['tour'] = big_events[0]
            turn_info['score'] = big_events[1]
            turn_info['ombre'] = big_events[2]
            turn_info['bloqué'] = big_events[3]
            turn_info['suspects'] = suspects.copy()
            for line in sub_turn.split('\n'):
                if line.startswith('QUESTION : '):
                    question.parse_question(line[11:])
                    if question.type == Type.DRAW:
                        next_value = 'personnage joué'
                    elif question.type == Type.POSITION:
                        next_value = 'position'
                    elif question.type == Type.POWER:
                        next_value = 'pouvoir utilisé'
                    else:
                        next_value = 'autre'
                if line.startswith('REPONSE INTERPRETEE : '):
                    turn_info[next_value] = line[22:]
                if line.startswith('NOUVEAU PLACEMENT : '):
                    nouveau_placement = line[20:]
                    for i, suspect in enumerate(suspects):
                        if suspect.startswith(nouveau_placement[:nouveau_placement.find('-')]):
                            suspects[i] = nouveau_placement
            all_turns_info.append(turn_info)
            pass
        pass
    return all_turns_info
