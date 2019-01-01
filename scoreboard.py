from dieexception import DieException

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
                "yahtzee": None,
                "chance": None,
                "yahtzeebonus": None,
            },
            "total lower": None,
            "grand total": None
        }

    def __add_section(self, section):
        """
        Sums all the values in a section (lower or upper) of the score dictionary
        """
        subtotal = 0
        for key in self.__score[section].keys():
            value = self.__score[section][key]
            if value is not -1:
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
        if not self.__field_is_blank('lower', 'yahtzee bonus'):
            subtotal += 100 * self.__score['lower']['yahtzee bonus']
        return subtotal

    def grandtotal(self):
        """
        Sums the top and bottom
        """
        return self.__score['total upper'] + self.__score['total lower']

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
                s = 0
            print(f'\t{score.capitalize()}: {s}')
    
    def get_keys(self):
        return list(self.__score.keys()) + list(self.__score['upper'].keys()) + list(self.__score['lower'].keys())
