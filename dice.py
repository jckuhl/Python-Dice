from random import randint

class Dice:

    """
    Models a single dice with x sides
    """

    value = 0
    def __init__(self, sides):
        """
        Initializes a dice with argument 'side' sides
        """
        self.sides = sides
    
    def roll(self):
        """
        rolls the dice to a random number between 1 and self.sides
        """
        self.value = randint(1, self.sides)
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '|[' + str(self.value) + ']|'

    def __eq__(self, other):
        """
        Checks equality by comparing value
        """
        if isinstance(other, Dice):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __ne__(self, other):
        """
        Checks equality by comparing value
        """
        if isinstance(other, Dice):
            return self.value != other.value
        elif isinstance(other, int):
            return self.value != other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')
    
    def __ge__(self, other):
        """
        Checks greater than or equal to by comparing value
        """
        if isinstance(other, Dice):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __gt__(self, other):
        """
        Checks greater than by comparing value
        """
        if isinstance(other, Dice):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __le__(self, other):
        """
        Checks less than or equal to by comparing value
        """
        if isinstance(other, Dice):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __lt__(self, other):
        """
        Checks less than by comparing value
        """
        if isinstance(other, Dice):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __add__(self, other):
        """
        adds two dice
        """
        if isinstance(other, Dice):
            return self.value + other.value
        elif isinstance(other, int):
            return self.value + other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __radd__(self, other):
        """
        adds two dice, reflexive
        """
        if isinstance(other, Dice):
            return self.value + other.value
        elif isinstance(other, int):
            return other + self.value
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')

    def __sub__(self, other):
        """
        subtracts two dice
        """
        if isinstance(other, Dice):
            return self.value - other.value 
        elif isinstance(other, int):
            return self.value - other
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')
        
    def __rsub__(self, other):
        """
        subtracts two dice
        """
        if isinstance(other, Dice):
            return other.value - self.value
        elif isinstance(other, int):
            return other - self.value
        else:
            raise TypeError(f'Invalid Types, must be a dice and a dice or int, recieved {type(other)}')
