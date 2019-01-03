from functools import partial
from dieexception import DieException
from operator import itemgetter
from pyzheecup import PyZhee

responses = {
    'yes': [
        'y',
        'yes',
    ],
    'no': [
        'n',
        'no'
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

def loop_multi_player(players, index, dicecup):
    """
    Primary gameplay loop, goes for 13 rounds per player
    """
    player = players[index]
    global pyzhee
    pyzhee = dicecup
    print(f'It is {player.name}\'s turn!')
    rolls = roll_die(pyzhee.roll_all, player.name)
    remaining_rolls = 2
    while remaining_rolls > 0:
        print(f'{player.name} has {remaining_rolls} rolls remaining.')
        response = input('Would you like to roll again? [Y/N]')
        if response.lower() in responses['yes']:
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
        elif response.lower() in responses['no']:
            remaining_rolls = 0
        else:
            print('Please only enter Y (yes) or N (no) as a response')
    apply_score(player, rolls)

def loop_ai(players, turns, dicecup):
    """
    Primary gameplay loop against AI
    """
    global pyzhee
    pyzhee = dicecup
    if turns % 2 == 0:
        player = players[0]
        print(f'It is {player.name}\'s turn!')
        #TODO player's turn
    else:
        player = players[1]
        print(f'It is {player.name}\'s turn!')
        pass
        #TODO computer's turn
    