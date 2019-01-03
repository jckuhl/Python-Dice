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

## dice.py

### `class Dice`

Models a single die.  A die may have an number of sides.  A two sided die would essentially be a coin.  Dice have the appropriate dunders to be added, subtracted and compared.  The initializer takes a single parameter, `sides`, the number of sides

```python
dice = Dice(6)  # six sided dice
dice.roll()     # produces a random value 1 <= x <= 6
```

> Unrolled dice have an initial value of zero

#### `roll()`

Rolls the die, returning a value between one and the number of sides, including both values.

## dicecup.py

### `class DiceCup`

Models a dice cup, like a Yahtzee cup.  Initializer takes a string in the format of XdY to generate dice, where X is the number of dice and Y is the number of sides on a dice.  For a Yahtzee game, for example, the string is `'5d6'`.  5 for five dice and 6 for six sides per die.

```python
dc = DiceCup('5d6') # create a dice cup with 5 six sided die
```

> Note that initializing the dice cup leaves all the dice unrolled with values of 0.

#### `roll_all()`

Rolls all the dice in the dice cup.  Returns `values` list

#### `roll_single(index)`

Rolls the die at a given index.  Returns `values` list

#### `roll_specific(number)`

Rolls all the dice within the cup that have the same value as the number passed in.  Returns `values` list

#### `roll_set(indices)`

Rolls all the dice with the given indices in the list passed in.  Throws an exception if any of the indices are out of bounds

#### `sum()`

Returns the sum of all the die

#### `count()`

Returns a dictionary where all the keys are the unique dice face (`dice.value`) and all the values are the number of occurances of each dice face.

#### `count_number(number)`

Counts the number of times `number` appears.  Basically a getter for `count()`

#### `sort(reverse=True)`

Sorts the dice in place, highest to lowest unless reverse is `False`, default is `True`

## pyzheecup.py

### `class PyZhee`

Inherits from `DiceCup` to be a specific implementation for a Yatzhee like game called PyZhee.  Initializes a DiceCup object with `5d6` immediately (five six sided die).

#### `find_kinds(num)`

Searches for `num` of a kind.  For example `pyzhee.find_kinds(3)` will find any "3 Of A Kinds" in the dice.  Returns a tuple with the value searched for and the number that repeats.

An example:

```python
pyzhee = PyZhee()
pyzhee.roll_all()
# [4, 4, 3, 3, 1]
pyzhee.find_kinds(2)
# [(4, 2), (3, 2)]
```

#### `of_a_kind(num)`

Similar to find kinds, returns `True` or `False` if a kind of `num` length is found

```python
pyzhee = PyZhee()
pyzhee.roll_all()
# [4, 4, 3, 3, 3]
pyzhee.of_a_kind(3)
# True
pyzhee.of_a_kind(4)
# False
```

#### `full_house()`

Returns `True` if a full house is present, `False` if not

#### `straight()`

Returns the length of a straight.  Because it finds a straight by detecting if the distance of two values in a sorted array is 1 (absolute value) or not, it will always be one less than the actual length.  A length of 3 means the straight has four digits

#### `sm_straight()`

Returns true if a straight with four dice (`straight()` returns `3` or higher) is present, false if not

#### `lg_straight()`

Returns true if a straight with five dice (`straight()` returns `4`) is present, false if not

#### `odd_man_out()`

Returns the value of the die that doesn't fit in with a straight, if there is a small straight.  `None` if there is no straight, or if there's a large straight.