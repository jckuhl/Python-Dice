number = {
    'ones': 1,
    'twos': 2,
    'threes': 3,
    'fours': 4,
    'fives': 5,
    'sixes': 6
}

lower_no_chance = {
    'three of a kind': 'sum',
    'four of a kind': 'sum',
    'pyzhee': 50,
    'small straight': 30,
    'large straight': 40,
    'full house': 25
}

def get_key_from_number(n):
    for k, v in number.items():
        if v == n:
            return k