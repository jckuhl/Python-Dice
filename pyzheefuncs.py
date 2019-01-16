import sys
import time
from functools import partial
from dieexception import DieException
from operator import itemgetter
from pyzheecup import PyZhee

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
    Example:  Bob scored 50 using Yatzhee
    """
    return f'{player.name} scored {score} using {field.title()}'

def set_score(player, key):
    """
    Scores the numbers in the upper section
    """
    number = {
        'ones': 1,
        'twos': 2,
        'threes': 3,
        'fours': 4,
        'fives': 5,
        'sixes': 6
    }
    n = number[key]
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
        if player.score_board.get_field('yatzhee') == None:
            if pyzhee.of_a_kind(5):
                score = player.score_board.set_score('yatzhee', 50)
                print('PYZHEE!')
                print(score_string(player, score, 'yatzhee'))
            else:
                score = player.score_board.set_score('yatzhee', 0)
                print('You\'ve lost your Yatzhee slot')
                print('WOMP womp wooooomp')
        elif player.score_board.get_field('yatzhee') == 50:
            # if the value is zero, the player filled it in with junk
            yahtzee_bonus = player.score_board.get_field('yatzhee bonus')
            if yahtzee_bonus == None:
                score = player.set_score('yatzhee bonus', 100)
            else:
                score = player.set_score('yatzhee bonus', 100 + yahtzee_bonus)
            print(score_string(player, score, 'yatzhee bonus'))

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
    if response == 'yatzhee bonus':
        print('You may only use that field if you\'ve already got a yatzhee and only for further yatzhees')
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
        'yatzhee': partial(of_a_kind, player, 5),
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
    print(f'{player_name} rolls: {rolls}')
    return rolls

def ai_loop(player):
    """
    Decision tree and loop for the ai
    I use the word "tree" here very liberally
    """
    def field_is_blank(field):
        """ Determine if a field is blank or not """
        return player.score_board.get_field(field) is None
    upper = {
        '1': 'ones',
        '2': 'twos',
        '3': 'threes',
        '4': 'fours',
        '5': 'fives',
        '6': 'sixes'
    }
    print(f'It is {player.name}\'s turn!')
    roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while True:
        print(f'{player.name} has {remaining_rolls} rolls remaining.')
        # Yatzhee
        if pyzhee.of_a_kind(5) and field_is_blank('yatzhee'):
            score = player.score_board.set_score('yatzhee', 50)
            print('PYZHEE!')
            print(score_string(player, score, 'yatzhee'))
            break

        # Yatzhee Bonus
        elif pyzhee.of_a_kind(5) and not field_is_blank('yatzhee'):
            yatzhee_bonus = player.score_board.get_field('yatzhee bonus')
            if yatzhee_bonus == None:
                score = player.score_board.set_score('yatzhee bonus', 100)
                print(score_string(player, score, 'yatzhee bonus'))
            else:
                score =player.score_board.set_score('yatzhee bonus', yatzhee_bonus + 100)
                print(score_string(player, score, 'yatzhee bonus'))
            break
        
        # Four of a Kind
        elif pyzhee.of_a_kind(4) and field_is_blank('four of a kind'):
            if field_is_blank('yatzhee') and remaining_rolls > 0:
                odd_man = pyzhee.not_a_kind(4)[0]
                pyzhee.roll_single(odd_man)
                remaining_rolls -= 1
            else:
                score = player.score_board.set_score('four of a kind', pyzhee.sum())
                print(score_string(player, score, 'four of a kind'))
                break

        # Full House
        elif pyzhee.full_house() and field_is_blank('full house'):
            # sometimes 3 of a kind is worth more than FH
            if pyzhee.sum > 25 and field_is_blank('three of a kind'):
                score = player.score_board.set_score('three of a kind', pyzhee.sum())
                print(score_string(player, score, 'three of a kind'))
            else:
                score = player.score_board.set_score('full house', 25)
                print(score_string(player, score, 'full house'))
            break

        # Three Of A Kind
        elif pyzhee.of_a_kind(3) and field_is_blank('three of a kind'):
            if remaining_rolls > 0 and (field_is_blank('yatzhee') or field_is_blank('four of a kind') or field_is_blank('full house')):
                odd_men = pyzhee.not_a_kind(3)
                pyzhee.roll_values(odd_men)
                remaining_rolls -= 1
            else:
                score = player.score_board.set_score('three of a kind', pyzhee.sum())
                print(score_string(player, score, 'three of a kind'))
                break

        # Large Straight
        elif pyzhee.lg_straight() and field_is_blank('large straight'):
            score = player.score_board.set_score('large straight', 40)
            print(score_string(player, score, 'large straight'))
            break

        # Small Straight
        elif pyzhee.sm_straight() and field_is_blank('small straight'):
            if remaining_rolls == 0:
                if pyzhee.sum() > 30 or not field_is_blank('chance'):
                    score = player.score_board.set_score('chance', pyzhee.sum())
                    print(score_string(player, score, 'chance'))
                else:
                    score = player.score_board.set_score('small straight', 30)
                    print(score_string(player, score, 'small straight'))
                break
            else:
                print(f'{player.name} is thinking . . .')
                time.sleep(1)
                odd_man = pyzhee.odd_man_out()
                index = pyzhee.get_die_index(odd_man)
                pyzhee.roll_single(index)
                remaining_rolls -= 1
        elif pyzhee.of_a_kind(2) and remaining_rolls > 0:
            pairs = pyzhee.find_kinds(2)    #[(value, number_of_occurances)]
            # if there are two pairs try for something better
            if len(pairs) == 2:
                odd_man = pyzhee.not_a_kind(2)[0]
                index = pyzhee.get_die_index(odd_man)
                pyzhee.roll_single(index)
                remaining_rolls -= 1
            # if there's one pair, and it's higher than 3
            elif pairs[0][0] > 3:
                pyzhee.roll_except(pairs[0][0])
                remaining_rolls -= 1
            else:
                pyzhee.roll_all()
                remaining_rolls -= 1
        # Chance and the upper part of the scoreboard
        else:
            if remaining_rolls == 0:
                if field_is_blank('chance'):
                    chance = pyzhee.sum()
                    upper_scores = [pyzhee.count_numbers(value) * value for value in upper.values()]
                    use_chance = True
                    for value in upper_scores:
                        if chance < value:
                            use_chance = False
                    if use_chance:
                        score = player.score_board.set_score('chance', chance)
                    else:
                        pass
                break

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
    