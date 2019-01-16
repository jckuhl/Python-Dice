from dice import Dice
from dieexception import DieException

dicecup_errors = {
    "invalid_string": DieException('Invalid dice type string, should be in format XdY'),
    "no_dice": DieException('No dice!')
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

    def set_values(self, values):
        """
        Sets all the values of the dice, mostly for debugging
        """
        if len(values) != len(self.dice):
            raise DieException(f'Values and dice must be the same length: {len(self.dice)}')
        index = 0
        for die in self.dice:
            die.value = values[index]
            index += 1
        return self.dice

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
            raise DieException(f'Invalid index: {index}')
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

    def roll_values(self, values):
        """
        Rolls all the dice that are in the values list given
        """
        include = self.get_die_indices(values)
        for index in self.get_die_indices(self.values):
            if index in include:
                self.values[index] = self.dice[index].roll()
        return self.values

    def roll_specific(self, number):
        """
        Rolls all the die with a specific value
        """
        for die in self.dice:
            if die == number:
                value = die.value
                roll = die.roll()
                index = self.values.index(value)
                self.values[index] = roll
        return self.values

    def roll_except(self, number):
        """
        Rolls all except the given number
        """
        for die in self.dice:
            if die != number:
                value = die.value
                roll = die.roll()
                index = self.values.index(value)
                self.values[index] = roll
        return self.values

    def roll_except_all(self, values):
        """
        Rolls all except the given list of dice
        """
        exclude = self.get_die_indices(values)
        for index in self.get_die_indices(self.values):
            if index not in exclude:
                self.values[index] = self.dice[index].roll()
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
        Sorts the dice, ascending if bool reverse is True
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