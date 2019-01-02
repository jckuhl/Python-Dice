from sys import argv
from functools import partial
from player import Player
from pyzheecup import PyZhee
from dieexception import DieException
from operator import itemgetter

def score_string(player, score, field):
    return f'{player.name} scored {score} using {field.title()}'

def set_score(player, key):
    number = {
        'ones': 1,
        'twos': 2,
        'threes': 3,
        'fours': 4,
        'fives': 5,
        'sixes': 6
    }
    try:
        n = number[key]
        player.score_board.set_score(key, pyzhee.count_numbers(n) * n)
    except DieException:
        print('Wrong')

def of_a_kind(player, value):

    def score_kind(field, score):
        if pyzhee.of_a_kind(score):
            score = player.score_board.set_score(field, pyzhee.sum())
        else:
            score = player.score_board.set_score(field, 0)
        print(score_string(player, score, field))
        return score

    if value == 3:
        score = score_kind('three of a kind', 3)
    elif value == 4:
        score = score_kind('four of a kind', 4)
    elif value == 5:
        score = score_kind('yahtzee', 50)
        if score == 50:
            print('PYZHEE!')
        else:
            print('WOMP womp wooooomp')

def find_straight(player, size):
    def score_straight(straight_fn, field, score):
        if straight_fn():
            score = player.score_board.set_score(field, score)
        else:
            score = player.score_board.set_score(field, 0)

    if size == 's':
        score_straight(pyzhee.sm_straight, 'small straight', 30)
    else:
        score_straight(pyzhee.lg_straight, 'large straight', 40)

def chance(player):
    score = player.score_board.set_score('chance', pyzhee.sum())
    print(score_string(player, score, 'chance'))

def score_full_house(player):
    if pyzhee.full_house():
        score = player.score_board.set_score('full house', 25)
        print(score_string(player, score, 'full house'))
    else:
        score = player.score_board.set_score('full house', 0)

def calc_score(player, response):
    scoreboard = {
        'ones': partial(set_score, player, 'ones'),
        'twos': partial(set_score, player, 'twos'),
        'threes': partial(set_score, player, 'threes'),
        'fours': partial(set_score, player, 'fours'),
        'fives': partial(set_score, player, 'fives'),
        'sixes': partial(set_score, player, 'sixes'),
        'three of a kind': partial(of_a_kind, player, 3),
        'four of a kind': partial(of_a_kind, player, 4),
        'full house': partial(score_full_house, player),
        'small straight': partial(find_straight, player, 's'),
        'large straight': partial(find_straight, player, 'l'),
        'yahtzee': partial(of_a_kind, player, 5),
        'chance': partial(chance, player)
    }
    scoreboard[response]()
    player.score_board.view_scores()

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
    rolls = roll_fn()
    print(f'{player_name} rolls: {rolls}')
    return rolls

def loop(players, index):
    """
    Primary gameplay loop, goes for 13 rounds per player
    """
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
                    # because visually the indexes need to match position, subtract 1 so list starts at 1
                    indices = list(map(lambda x: int(x) - 1,list(response)))
                    try:
                        rolls = roll_die(partial(pyzhee.roll_set, indices), player.name)
                        break
                    except DieException:
                        print('Please chose a valid position between 1-5')
                else:
                    print('Invalid response')
        elif response.lower() == 'n':
            remaining_rolls = 0
        else:
            print('Please only enter Y (yes) or N (no) as a response')
    apply_score(player, rolls)

def game(players):
    """
    Starts, runs and ends the game
    """
    global pyzhee
    num_players = len(players)
    pyzhee = PyZhee()
    pyzhee.roll_all()
    print('Welcome to PyZhee!')
    index = 0
    turns = num_players * 13
    while turns > 0:
        loop(players, index)
        index += 1
        if index >= num_players:
            index = 0
        turns -= 1
    print('Game over!')
    final_scores = [(player.name, player.score_board.get_grand_total()) for player in players]
    winner = max(final_scores, key=itemgetter(1))
    print(f'{winner[0]} wins with a score of {winner[1]}')
    print(f'Thank you for playing!')

if __name__ == "__main__":
    names = argv[1:]
    if len(names) > 1:
        players = []
        for name in names:
            players.append(Player(name.capitalize()))
        game(players)
    else:
        print(len(names))
        