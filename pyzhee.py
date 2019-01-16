from sys import argv
from player import Player
from pyzheegame import game
from pyzheegameai import gameai
from scoreboard import ScoreBoard
from random import choice

ai_players = [
    'Guido Van Rossum',
    'Alan Turing',
    'Dennis Ritchie',
    'Larry Wall',
    'Yukihiro Matsumoto',
    'Bjarne Stroustrup',
    'Linus Torvalds',
    'Ken Thompson',
    'Grace Hopper',
    'Ada Lovelace',
    'Margaret Hamilton',
    'John Von Neumann'
]

if __name__ == "__main__":
    names = argv[1:]
    players = []
    if len(names) > 1:
        for name in names:
            players.append(Player(name.capitalize(), ScoreBoard))
        game(players)
    else:
        if len(argv) == 1:
            player = Player('Player 1', ScoreBoard)
        else:
            player = Player(argv[1].capitalize(), ScoreBoard)
        players.extend([player, Player(choice(ai_players), ScoreBoard)])
        gameai(players)
        