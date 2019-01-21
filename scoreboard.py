import scoreboard_dict
from dieexception import DieException
from dict_util import get_max, get_min

class ScoreBoard:

    def __init__(self):
        """
        Initializes a scoreboard with a set up for the score dictionary
        """
        self.__score = {
            "upper": {
                "ones": None,
                "twos": None,
                "threes": None,
                "fours": None,
                "fives": None,
                "sixes": None,
            },
            "total upper": None,
            "lower": {
                "three of a kind": None,
                "four of a kind": None,
                "full house": None,
                "small straight": None,
                "large straight": None,
                "yatzhee": None,
                "chance": None,
                "yatzhee bonus": None,
            },
            "total lower": None,
            "grand total": None
        }

    def __add_section(self, section):
        """
        Sums all the values in a section (lower or upper) of the score dictionary
        None values are treated as zero
        """
        subtotal = 0
        for key in self.__score[section].keys():
            value = self.__score[section][key]
            if value is not None:
                subtotal += self.__score[section][key]
            else:
                subtotal += 0
        return subtotal

    def __field_is_blank(self, *args):
        """
        Checks if a given field is blank.  *args are keys given in order
        Example: self.__field_is_blank('lower', 'ones') will check for none on self.__score['lower']['ones']
        """
        if len(args) == 2:
            return self.__score[args[0]][args[1]] == None
        elif len(args) == 1:
            return self.__score[args[0]] == None
        else:
            raise Exception('invalid number of arguments')

    def total_upper(self):
        """
        Sums the upper section, adding 35 as a bonus if the score is greater than 63
        """
        subtotal = self.__add_section('upper')
        if subtotal >= 63:
            subtotal += 35
        return subtotal


    def total_lower(self):
        """
        Sums the lower section, adding 100 * the number of yahtzee bonuses, if there are any
        """
        subtotal = self.__add_section('lower')
        if not self.__field_is_blank('lower', 'yatzhee bonus'):
            subtotal += 100 * self.__score['lower']['yahtzee bonus']
        return subtotal

    def calculate_totals(self):
        """
        Sums the upper and lower sections, the grand total, and sets them
        """
        self.__score['total upper'] = self.total_upper()
        self.__score['total lower'] = self.total_lower()
        self.__score['grand total'] = self.__score['total upper'] + self.__score['total lower']
        return self.__score['grand total']

    def set_score(self, key, value):
        """
        Sets a field's score if it isn't blank
        """
        if key in self.__score['upper'].keys():
            if not self.__field_is_blank('upper', key):
                raise DieException('That field is not blank!')
            else:
                self.__score['upper'][key] = value
        elif key in self.__score['lower'].keys():
            if not self.__field_is_blank('lower', key):
                raise DieException('That field is not blank!')
            else:
                self.__score['lower'][key] = value
        return value

    def view_scores(self):
        """
        Prints out the scores
        """
        scores = { 
            **self.__score['upper'],
            'total upper': self.__score['total upper'],
            **self.__score['lower'],
            'total lower': self.__score['total lower'],
            'grand total': self.__score['grand total'] 
        }
        for score in scores:
            s = scores[score]
            if s == None:
                s = 'blank'
            print(f'\t{score.title()}: {s}')
    
    def get_keys(self):
        return list(self.__score.keys()) + list(self.__score['upper'].keys()) + list(self.__score['lower'].keys())

    def get_grand_total(self):
        return self.__score['grand total']

    def get_field(self, field):
        if field in self.__score['upper']:
            return self.__score['upper'][field]
        elif field in self.__score['lower']:
            return self.__score['lower'][field]
        elif field in self.__score:
            return self.__score[field]
        else:
            return False

    def field_is_blank(self, field):
        """ Determine if a field is blank or not """
        return self.get_field(field) is None

    def get_all_empty_fields(self):
        """ Get a dictionary of empty fields """
        empty = {}
        exclude = ['total upper', 'total lower', 'yatzhee bonus', 'grand total']
        for key in self.get_keys():
            if self.field_is_blank(key) and key not in exclude:
                value = self.get_field(key)
                empty.update({ key: value })
        return empty

    def calc_possible_upper_scores(self, pyzhee):
        """
        Returns the possible scores the player can get with the current dice.
        PyZhee is a pyzhee object with a count_numbers method
        """
        upper = self.get_field('upper')
        empty_upper = {}
        # populate empty_upper with the scores player will recieve if she plays there
        for field in upper:
            if self.field_is_blank(field):
                n = scoreboard_dict.number[field]
                empty_upper[field] = n * pyzhee.count_numbers(n)
        return empty_upper

    def get_min_max_lower(self, pyzhee, min_val=True):
        lower = self.get_field('lower')
        empty_lower = {}
        for field in lower:
            if self.field_is_blank(field):
                value = scoreboard_dict.lower_no_chance[field]
                value = pyzhee.sum() if value == 'sum' else value
                empty_lower.update({field: value})
        return get_min(empty_lower) if min_val else get_max(empty_lower)