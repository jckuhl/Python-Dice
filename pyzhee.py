import sys
from player import Player
from pyzheecup import PyZhee
from dice import Dice

def loop(players, index):
    if index >= num_players:
        return False
    player = players[index]
    print(f'It is {player.name}\'s turn!')
    print(f'{player.name} rolls: ')
    rolls = pyzhee.roll_all()
    print(rolls)

    if index < num_players:
        index += 1
    # if index >= num_players:
    #     index = 0
    return loop(players, index)

def game(players):
    global num_players, pyzhee
    num_players = len(players)
    pyzhee = PyZhee()
    pyzhee.roll_all()
    print('Welcome to PyZhee!')
    index = 0
    while loop(players, index):
        pass
    print('Game over!')


if __name__ == "__main__":
    names = sys.argv[1:]
    if len(names) > 0:
        players = []
        for name in names:
            players.append(Player(name))
        game(players)
    else:
        print(len(names))
        