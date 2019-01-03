from dice import Dice
from dieexception import DieException

dicecup_errors = {
    "invalid_string": Exception('Invalid dice type string, should be in format XdY'),
    "no_dice": Exception('No dice!')
}

class DiceCup:

    """
    Models a dice holder
    """

    def __init__(self, dice_type):
        """
        Initializes a dice holder with a string of XdY where X is the number of dice and Y is the number of sides per dice
        """
        dice_type = dice_type.split('d')
        if len(dice_type) != 2:
            raise dicecup_errors["invalid_string"]
        dice = int(dice_type[0])
        sides = int(dice_type[1])
        self.dice = []
        self.values = []
        while len(self.dice) < dice:
            self.dice.append(Dice(sides))

    def roll_all(self):
        """
        Rolls all the dice in the cup, raises an exception if there are no dice in the cup
        """
        if len(self.dice) == 0:
            raise dicecup_errors["no_dice"]
        self.values = []
        for die in self.dice:
            self.values.append(die.roll())
        return self.values

    def roll_single(self, index):
        """
        Rolls a die at a specific index
        """
        if len(self.dice) == 0:
            raise dicecup_errors["no_dice"]
        if index >= len(self.dice) or index < 0:
            raise DieException()
        self.values[index] = self.dice[index].roll()
        return self.values

    def roll_set(self, indices):
        """
        Rolls at a given list of indices
        """
        for index in indices:
            if index >= len(self.dice) or index < 0:
                raise DieException()
        for index in indices:
            self.values[index] = self.dice[index].roll()
        return self.values

    def roll_specific(self, number):
        """
        Rolls all the die with a specific value
        """
        for die in self.dice:
            if die.value == number:
                die.roll()
        return self.values

    def sum(self):
        """
        Adds all the dice up
        """
        if len(self.dice) == 0:
            raise dicecup_errors["no_dice"]
        result = 0
        for die in self.dice:
            result += die
        return result

    def count(self):
        """
        Counts the occurrance of each number, returns a dictionary, { value: count_of_value }
        """
        if len(self.dice) == 0:
            raise dicecup_errors["no_dice"]
        counter = {}
        for die in self.dice:
            key = str(die)
            if key not in counter:
                counter[key] = 1
            else:
                counter[key] += 1
        return counter

    def count_numbers(self, number):
        """
        Counts how many times the number passed in appears
        """
        number = str(number)
        count = self.count()
        if number in count.keys():
            return count[number]
        else:
            return 0

    def sort(self, reverse=True):
        """
        sorts the dice, ascending if bool reverse is True
        """
        self.dice.sort(reverse=reverse)
        return self.dice

    def get_die_index(self, value):
        """
        Gets the index of a given value or a -1 if it isn't found
        """
        try:
            return self.dice.index(value)
        except ValueError:
            return -1

    def get_die_indices(self, values):
        """
        Gets the indices of all values found from a list of values
        """
        indices = []
        for value in values:
            i = self.get_die_index(value)
            if i != -1:
                indices.append(i)
        return indices