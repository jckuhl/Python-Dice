# PyDie

A Framework for making dice game.  Primary modules are `dice.py` and `dicecup.py`.

A Yahtzee clone can be played from `pyzhee.py` and uses `scoreboard.py` and `pyzheecup.py`.

Play `pyzhee` by entering the following commands:

```
python3 pyzhee.py player1 player2 player3
```
- This will set up a game between three players.  Each argument is a player's name: 
    - `python3 pyzhee.py michael pam jim dwight`
- You may have as many players as you wish
- python3 can be replaced by whatever your path to Python 3 is in your system
- Providing zero or one arguments will have you play against a computer opponent
    - Without providing a name, you'll simply be refered to as 'Player 1'

Please see [How to play](howtoplay.md) for more information

## dice.py

> For brevity sake, I will be ignoring the `self` argument in all method headers as it is only relevant inside the class

### `class Dice`

Models a single die.  A die may have an number of sides.  A two sided die would essentially be a coin.  Dice have the appropriate dunders to be added, subtracted and compared.  The initializer takes a single parameter, `sides`, the number of sides

```python
>>> dice = Dice(6)  # six sided dice
>>> dice.roll()     # produces a random value 1 <= x <= 6
3
>>> dice.roll()
5
```

> Unrolled dice have an initial value of zero

#### `roll()`

Rolls the die, returning a value between one and the number of sides, including both values.

## dicecup.py

### `class DiceCup`

Models a dice cup, like a Yahtzee cup.  Initializer takes a string in the format of XdY to generate dice, where X is the number of dice and Y is the number of sides on a dice.  For a Yahtzee game, for example, the string is `'5d6'`.  5 for five dice and 6 for six sides per die.

```python
>>> dicecup = DiceCup('5d6') # create a dice cup with 5 six sided die
```

> Note that initializing the dice cup leaves all the dice unrolled with values of 0.

#### `set_values(values)`

Sets the values of the dice cup to the values given.  Must be a list equal to the number of die in the dice cup.

> This method was designed primarily for unit testing, it doesn't actually roll any of the die

```python
>>> dicecup.set_values([1,1,1,1,1])
[1, 1, 1, 1, 1]
```

#### `roll_all()`

Rolls all the dice in the dice cup.  Returns `values` list

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
```

#### `roll_single(index)`

Rolls the die at a given index.  Returns `values` list

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_single(0)
[3, 4, 3, 2, 3]
```

#### `roll_specific(number)`

Rolls all the dice within the cup that have the same value as the number passed in.  Returns `values` list

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_specific(3)
[1, 4, 6, 2, 5]
```

#### `roll_set(indices)`

Rolls all the dice with the given indices in the list passed in.  Throws an exception if any of the indices are out of bounds.

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_set([0, 1, 2])
[6, 2, 4, 2, 3]
```

#### `roll_values(values)`

Rolls all the dice with the given list of values passed in.  Throws an exception if any of the indices are out of bounds.

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_values([4, 3])
[1, 2, 4, 2, 6]
```

#### `roll_except(number)`

Rolls all the dices whose value does not match the given number

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_except(3)
[5, 6, 3, 3, 3]
```

#### `roll_except_all(numbers)`

Rolls all the dice whose value is not in the given list of numbers

```python
>>> dicecup.roll_all()
[1, 4, 3, 2, 3]
>>> dicecup.roll_except_all([3, 4])
[5, 4, 3, 6, 3]
```

#### `sum()`

Returns the sum of all the die

```python
>>> dicecup.roll_all()
[1, 1, 1, 2, 2]
>>> dicecup.sum()
7
```

#### `count()`

Returns a dictionary where all the keys are the unique dice face (`dice.value`) and all the values are the number of occurances of each dice face.

```python
>>> dicecup.roll_all()
[3, 2, 2, 3, 3]
>>> dicecup.count()
{'3': 3, '2': 2}
```

#### `count_numbers(number)`

Counts the number of times `number` appears.  Basically a getter for `count()`

```python
>>> dicecup.roll_all()
[4, 2, 2, 4, 4]
>>> dicecup.count_numbers(4)
3
```

#### `sort(reverse=True)`

Sorts the dice in place, highest to lowest unless reverse is `False`, default is `True`

```python
>>> dicecup.roll_all()
[4, 2, 2, 4, 4]
>>> dicecup.sort()
[4, 4, 4, 2, 2]
>>> dicecup.sort(reverse=False)
[2, 2, 4, 4, 4]
```

#### `get_die_index(value)`

Gets the index of the first occurrence of a given value or `-1` if it isn't found

```python
>>> dicecup.roll_all()
[4, 2, 2, 4, 4]
>>> dicecup.get_die_index(2)
1
>>> dicecup.get_die_index(5)
-1
```

#### `get_die_indices(values)`

Returns a list of die indices for the list of values put in or an empty list if none are found

```python
>>> pyzhee.roll_all()
[3, 5, 6, 5, 4]
>>> pyzhee.get_die_indices([3,5,6])
[0, 1, 2]
```

## pyzheecup.py

### `class PyZhee`

Inherits from `DiceCup` to be a specific implementation for a Yatzhee like game called PyZhee.  Initializes a DiceCup object with `5d6` immediately (five six sided die).

#### `find_kinds(num)`

Searches for `num` of a kind.  For example `pyzhee.find_kinds(3)` will find any "3 Of A Kinds" in the dice.  Returns a tuple with the value searched for and the number that repeats.

An example:

```python
>>> pyzhee = PyZhee()
>>> pyzhee.roll_all()
[4, 4, 3, 3, 1]
>>> pyzhee.find_kinds(2)
[(4, 2), (3, 2)]
```

#### `of_a_kind(num)`

Similar to find kinds, returns `True` or `False` if a kind of `num` length is found

```python
>>> pyzhee = PyZhee()
>>> pyzhee.roll_all()
[4, 4, 3, 3, 3]
>>> pyzhee.of_a_kind(3)
True
>>> pyzhee.of_a_kind(4)
False
```

#### `full_house()`

Returns `True` if a full house is present, `False` if not

```python
>>> pyzhee.roll_all()
[3, 3, 3, 4, 4]
>>> pyzhee.full_house()
True
```

#### `straight()`

Returns the length of a straight.  Because it finds a straight by detecting if the distance of two values in a sorted array is 1 (absolute value) or not, it will always be one less than the actual length.  A length of 3 means the straight has four digits

```python
>>> pyzhee.roll_all()
[3, 2, 3, 4, 5]
>>> pyzhee.straight()
3
>>> pyzhee.roll_all()
[1, 2, 3, 4, 5]
>>> pyzhee.sm_straight()
4
```

#### `sm_straight()`

Returns true if a straight with four dice (`straight()` returns `3` or higher) is present, false if not

```python
>>> pyzhee.roll_all()
[3, 2, 3, 4, 5]
>>> pyzhee.sm_straight()
True
>>> pyzhee.sm_straight()
False
```

#### `lg_straight()`

Returns true if a straight with five dice (`straight()` returns `4`) is present, false if not

```python
>>> pyzhee.roll_all()
[1, 2, 3, 4, 5]
>>> pyzhee.sm_straight()
True
>>> pyzhee.lg_straight()
True
```

#### `odd_man_out()`

Returns the value of the die that doesn't fit in with a straight, if there is a small straight.  `None` if there is no straight, or if there's a large straight.

```python
>>> pyzhee.roll_all()
[1, 2, 3, 4, 6]
>>> pyzhee.odd_man_out()
[6]
```

#### `not_of_a_kind(kind)`

Similar to `odd_man_out()`.  Returns a list of values that don't match a specific _kind_.  `kind` indicates what sort of kind to look for.  If the function is passed a `3` for instance, it will return all the values that are _not_ in a three of a kind.

```python
>>> pyzhee.roll_all()
[2, 2, 2, 3, 1]
>>> pyzhee.not_of_a_kind(3)
[3, 1]
```

> `not_of_a_kind()` and `odd_man_out()` both return lists, even if there's only one value

## scoreboard.py

### class ScoreBoard

A Yatzhee specific scoreboard.  One single attribute, a `__score` dictionary which is meant to only be accessed through methods on the class.  Will not allow values to be rewritten if they're already written, which is why the attribute is meant to be private.

```python
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
```

Scoreboard is a property on the Player class.

```python
class Player:
    
    def __init__(self, name):
        self.name = name
        self.score_board = ScoreBoard()
```

#### `total_upper()`

Returns the total score for the upper section, adding 35 points if the score is 63 or higher.

#### `total_lower()`

Returns the total score for the lower section

#### `calculate_totals()`

Returns the total sum of all the scores and also sets them in the `__score` dictionary

#### `set_score(key, value)`

Sets a score at a given key, a specific value

```python
>>> player.scoreboard.set_score('large straight', 40)
```
> Throws DieException if the field already has a value

#### `get_keys()`

Gets the scoreboard's `__score` attribute's keys, as if the dictionary was flattened (without flattening the dictionary)

#### `get_grand_total()`

Returns the grand total

#### `get_field(field)`

Returns the value at a given field, `False` if nothing is found

```python
>>> player.scoreboard.get_field('yatzhee')
50
```