from sys import argv
from functools import partial
from player import Player
from pyzheecup import PyZhee
from dieexception import DieException

def set_score(player, key):
    number = {
        'ones': 1,
        'twos': 2,
        'threes': 3,
        'fours': 4,
        'fives': 5,
        'six': 6
    }
    try:
        player.score_board.set_score(key, pyzhee.count_numbers(number[key]))
    except DieException as e:
        print(e)
    player.score_board.view_scores()

def calc_score(player, response):
    scoreboard = {
        'ones': partial(set_score, player, 'ones'),
        'twos': partial(set_score, player, 'twos'),
        'threes': partial(set_score, player, 'threes'),
        'fours': partial(set_score, player, 'fours'),
        'fives': partial(set_score, player, 'fives'),
        'sixes': partial(set_score, player, 'sixes'),
    }
    scoreboard[response]()

def apply_score(player, rolls):
    """
    Allows the player to determine how to apply their score
    """
    print(f'Here are {player.name}\'s current scores: ')
    player.score_board.view_scores()
    while True:
        response = input('What field would you like to put your current score in?')
        response = response.lower()
        if response in player.score_board.get_keys():
            calc_score(player, response)
            break
        else:
            print('Please enter the desired field as it is displayed')

def create_roll_string(rolls):
    """
    Creates a string with the current roll so the player knows which index each die belongs to
    For the player's use, the index starts at 1 rather than 0
    """
    string = ''
    index = 1
    for roll in rolls:
        string += str(index) + ': [' + str(roll) + ']'
        index += 1
        if index <= len(rolls):
            string += ', '
    return string

def roll_die(roll_fn, player_name):
    """
    Rolls and displays the dice for a player
    """
    print(f'{player_name} rolls: ')
    rolls = roll_fn()
    print(rolls)
    return rolls

def loop(players, index):
    """
    Primary gameplay loop, goes for 13 rounds per player
    """
    if index >= num_players:
        return False
    player = players[index]
    print(f'It is {player.name}\'s turn!')
    rolls = roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while remaining_rolls > 0:
        print(f'{player.name} has {remaining_rolls} rolls remaining.')
        response = input('Would you like to roll again? [Y/N]')
        if response.lower() == 'y':
            remaining_rolls -= 1
            print('Here are the current values:')
            print(create_roll_string(rolls))
            while True:
                response = input('Enter the number for each dice you\'d like to reroll, or \'A\' to reroll all:\n')
                if response.lower() == 'a':
                    rolls = roll_die(pyzhee.roll_all, player.name)
                    break
                elif response.isdigit():
                    # TODO: if response out of bounds
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
    apply_score(player, rolls)
    if index < num_players:
        index += 1
    if index >= num_players:
        index = 0
    return True

def game(players):
    """
    Starts, runs and ends the game
    """
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
    names = argv[1:]
    if len(names) > 1:
        players = []
        for name in names:
            players.append(Player(name.capitalize()))
        game(players)
    else:
        print(len(names))
        