from sys import argv
from player import Player
from pyzheegame import game
from pyzheegameai import gameai

if __name__ == "__main__":
    names = argv[1:]
    if len(names) > 1:
        players = []
        for name in names:
            players.append(Player(name.capitalize()))
        game(players)
    else:
        if len(argv) == 1:
            player = Player('Player 1')
        else:
            player = Player(argv[1].capitalize())
        gameai(player)
        print(f'{player.name} playing against the AI!')
        