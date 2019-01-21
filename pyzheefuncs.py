import sys
import time
import scoreboard_dict
from functools import partial
from dieexception import DieException
from operator import itemgetter
from pyzheecup import PyZhee
from dict_util import get_max, get_min


responses = {
    'yes': [
        'y',
        'yes',
        'da'
    ],
    'no': [
        'n',
        'no',
        'nyet'
    ],
    'exit': [
        'exit',
        'quit',
        'q',
        'x',
        'e'
    ]
}

def score_string(player, score, field):
    """
    Creates a string that labels how a player scored.
    Example:  Bob scored 50 using PyZhee
    """
    return f'{player.name} scored {score} using {field.title()}'

def set_score(player, key):
    """
    Scores the numbers in the upper section
    """
    n = scoreboard_dict.number[key]
    score = player.score_board.set_score(key, pyzhee.count_numbers(n) * n)
    print(score_string(player, score, key))

def of_a_kind(player, value):
    """
    Scores 'of a kind' combinations
    """

    def score_kind(field, score):
        """
        Helper function that sets the score
        """
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
        if player.score_board.get_field('pyzhee') == None:
            if pyzhee.of_a_kind(5):
                score = player.score_board.set_score('pyzhee', 50)
                print('PYZHEE!')
                print(score_string(player, score, 'pyzhee'))
            else:
                score = player.score_board.set_score('pyzhee', 0)
                print('You\'ve lost your PyZhee slot')
                print('WOMP womp wooooomp')
        elif player.score_board.get_field('pyzhee') == 50:
            # if the value is zero, the player filled it in with junk
            yahtzee_bonus = player.score_board.get_field('pyzhee bonus')
            if yahtzee_bonus == None:
                score = player.set_score('pyzhee bonus', 100)
            else:
                score = player.set_score('pyzhee bonus', 100 + yahtzee_bonus)
            print(score_string(player, score, 'pyzhee bonus'))

def find_straight(player, size):
    """
    Scores a straight
    """
    def score_straight(straight_fn, field, score):
        """
        Helper function that sets straight score
        """
        if straight_fn():
            score = player.score_board.set_score(field, score)
            print(score_string(player, score, field))
        else:
            score = player.score_board.set_score(field, 0)

    if size == 's':
        score_straight(pyzhee.sm_straight, 'small straight', 30)
    else:
        score_straight(pyzhee.lg_straight, 'large straight', 40)

def chance(player):
    """
    Scores a chance
    """
    score = player.score_board.set_score('chance', pyzhee.sum())
    print(score_string(player, score, 'chance'))

def score_full_house(player):
    """
    Scores a full house
    """
    if pyzhee.full_house():
        score = player.score_board.set_score('full house', 25)
        print(score_string(player, score, 'full house'))
    else:
        score = player.score_board.set_score('full house', 0)

def calc_score(player, response):
    """
    Determines the appropriate function to run given the player's response
    """
    if response == 'pyzhee bonus':
        print('You may only use that field if you\'ve already got a pyzhee and only for further pyzhees')
        return False
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
        'pyzhee': partial(of_a_kind, player, 5),
        'chance': partial(chance, player)
    }
    if response not in scoreboard:
        print('Invalid response, please try again')
        return False
    try:
        scoreboard[response]()
        player.score_board.calculate_totals()
        player.score_board.view_scores()
        return True
    except DieException:
        print('That field has a value, please pick a blank one')
        return False

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
            successful_score = calc_score(player, response)
            if successful_score:
                break
        elif response in responses['exit']:
            sys.exit()
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
    print(f'{player_name} rolls: {pyzhee.values}')
    return rolls

def get_available_fields(player):
    available = player.score_board.get_all_empty_fields()
    # calculate all the possible scores and do the one on the top
    scoreboard = {
        'ones': lambda: pyzhee.count_numbers(1),
        'twos': lambda: pyzhee.count_numbers(2) * 2,
        'threes': lambda: pyzhee.count_numbers(3) * 3,
        'fours': lambda: pyzhee.count_numbers(4) * 4,
        'fives': lambda: pyzhee.count_numbers(5) * 5,
        'sixes': lambda: pyzhee.count_numbers(6) * 6,
        'three of a kind': lambda: pyzhee.sum() if pyzhee.of_a_kind(3) else 0,
        'four of a kind': lambda: pyzhee.sum() if pyzhee.of_a_kind(4) else 0,
        'full house': lambda: 25 if pyzhee.full_house() else 0,
        'small straight': lambda: 30 if pyzhee.sm_straight() else 0,
        'large straight': lambda: 40 if pyzhee.lg_straight() else 0,
        'chance': lambda: pyzhee.sum()
    }
    for key in available.keys():
        available[key] = scoreboard[key]()
    return available

def ai_chose_field(player):
    """
    AI choses a field to put their score into
    """
    if pyzhee.of_a_kind(5):
        # If PyZhee, either score in pyzhee or pyzhee bonus, then skip the rest of this function
        score = 0
        field = ''
        if player.score_board.field_is_blank('pyzhee'):
            score = player.score_board.set_score('pyzhee', 50)
            field = 'pyzhee'
        else:
            score = player.score_board.get_field('pyzhee bonus')
            score = score if score is not None else 0
            score = player.score_board.set_score('pyzhee bonus', score + 100)
            field = 'pyzhee bonus'
        print('PYZHEE!')
        print(score_string(player, score, field))
        return
    available = get_available_fields(player)
    key, value = get_max(available)
    if value == 0:
        sacrifice = {}
        for n in scoreboard_dict.number:
            if n in available:
                value = scoreboard_dict.number[n]
                sacrifice.update({ n: value})
        for n in scoreboard_dict.lower_no_chance:
            if n in available:
                value = scoreboard_dict.number[n]
                sacrifice.update({ n: pyzhee.sum() if value == 'sum' else value })
        key, value = get_min(sacrifice)
        if key == 'pyzhee':
            print('You\'ve lost your PyZhee slot')
            print('WOMP womp wooooomp')
        player.score_board.set_score(key, 0)
        print(score_string(player, 0, key))
    else:
        player.score_board.set_score(key, value)
        print(score_string(player, value, key))

def ai_chose_action(player):
    """
    Returns the indices of dice the player wants to reroll, if any
    'all' if the player wants to reroll all, 
    'score' if the player wants to score
    [indices] if the player wants to reroll some
    """
    # Handle pyzhee immediately so any set up can be skipped if there is one
    if pyzhee.of_a_kind(5):
        return 'score'

    available = get_available_fields(player)
    if pyzhee.lg_straight() and 'large straight' in available:
        return 'score'
    return 0

def ai_loop(player):
    """
    Decision tree and loop for the ai
    I use the word "tree" here very liberally
    """
    print(f'It is {player.name}\'s turn!')
    roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while True:
        print(f'{player.name} has {remaining_rolls} rolls remaining.')
        if remaining_rolls == 0:
            ai_chose_field(player)
            break
        else:
            dice = ai_chose_action(player)
            if dice == 'score':
                ai_chose_field(player)
                break
            elif dice == 'all':
                roll_die(pyzhee.roll_all, player.name)
            else:
                roll_die(partial(pyzhee.roll_set, dice), player.name)
            remaining_rolls -= 1

    player.score_board.calculate_totals()
    player.score_board.view_scores()


def player_loop(player):
    print(f'It is {player.name}\'s turn!')
    rolls = roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while remaining_rolls > 0:
        print(f'{player.name} has {remaining_rolls} rolls remaining.')
        response = input('Would you like to roll again? [Y/N]')
        response.lower()
        if response.lower() in responses['yes']:
            remaining_rolls -= 1
            print('Here are the current values:')
            print(create_roll_string(rolls))
            while True:
                response = input('Enter the number for each dice you\'d like to reroll, or \'A\' to reroll all:\n')
                response.lower()
                if response == 'a':
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
                elif response in responses['exit']:
                    sys.exit()
                else:
                    print('Invalid response')
        elif response in responses['no']:
            remaining_rolls = 0
        elif response in responses['exit']:
            sys.exit()
        else:
            print('Please only enter Y (yes) or N (no) as a response')
    apply_score(player, rolls)

def loop_multi_player(players, index, dicecup):
    """
    Primary gameplay loop, goes for 13 rounds per player
    """
    global pyzhee
    pyzhee = dicecup
    player = players[index]
    player_loop(player)

def loop_ai(players, turns, dicecup):
    """
    Primary gameplay loop against AI
    """
    global pyzhee
    pyzhee = dicecup
    if turns % 2 == 0:
        player = players[0]
        player_loop(player)
    else:
        player = players[1]
        ai_loop(player)
    