import sys
from functools import partial
from player import Player
from pyzheecup import PyZhee
from dicecup import DiceCup
from dice import Dice

def create_roll_string(rolls):
    string = ''
    index = 1
    for roll in rolls:
        string += str(index) + ': [' + str(roll) + ']'
        index += 1
        if index <= len(rolls):
            string += ', '
    return string

def roll_die(roll_fn, player_name):
    print(f'{player_name} rolls: ')
    rolls = roll_fn()
    print(rolls)
    return rolls

def loop(players, index):
    if index >= num_players:
        return False
    player = players[index]
    print(f'It is {player.name}\'s turn!')
    rolls = roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while remaining_rolls > 0:
        print(f'{player.name} has {remaining_rolls} remaining.')
        response = input('Would you like to roll again? [Y/N]')
        if response.lower() == 'y':
            remaining_rolls -= 1
            print('Here are the current values:')
            print(create_roll_string(rolls))
            while True:
                response = input('Enter the indexes for each dice you\'d like to reroll, or \'A\' to reroll all:\n')
                if response.lower() == 'a':
                    rolls = roll_die(pyzhee.roll_all, player.name)
                    break
                elif response.isdigit():
                    # because visually the indexes need to match position, subtract 1 so list starts at 1
                    indices = list(map(lambda x: int(x) - 1,list(response)))
                    rolls = roll_die(partial(pyzhee.roll_set, indices), player.name)
                    break
                else:
                    print('Invalid response')
        elif response.lower() == 'n':
            remaining_rolls = 0
        else:
            print('Please only enter Y (yes) or N (no) as a response')

    if index < num_players:
        index += 1
    if index >= num_players:
        index = 0
    return True

def game(players):
    global num_players, pyzhee
    num_players = len(players)
    pyzhee = PyZhee()
    pyzhee.roll_all()
    print('Welcome to PyZhee!')
    index = 0
    while True:
        looping = loop(players, index)
        index += 1
        if not looping:
            break
    print('Game over!')


if __name__ == "__main__":
    names = sys.argv[1:]
    if len(names) > 1:
        players = []
        for name in names:
            players.append(Player(name.capitalize()))
        game(players)
    else:
        print(len(names))
        