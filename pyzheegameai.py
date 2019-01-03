from pyzheecup import PyZhee
from pyzheefuncs import loop_ai

def gameai(players):
    print('Welcome to PyZhee, single player mode')
    print(f'Your opponent is {players[1].name}')
    pyzhee = PyZhee()
    turns = 0
    while turns < 26:
        loop_ai(players, turns, pyzhee)
        turns += 1
    
    