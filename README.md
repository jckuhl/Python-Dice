# PyDie

A Framework for making dice game.  Primary modules are `dice.py` and `dicecup.py`.

A Yahtzee clone can be played from `pyzhee.py` and uses `scoreboard.py` and `pyzheecup.py`.

Play `pyzhee` by entering the following commands:

```
python3 pyzhee.py player1 player2 player3
```
- This will set up a game between three players.  Each argument is a player's name
- You may have as many players as you wish
- python3 can be replaced by whatever your path to Python 3 is in your system
- Providing zero arguments will have you play against a computer opponent

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

#### `roll_set(number)`

Rolls all the dice within the cup that have the same value as the number passed in.  Returns `values` list

#### `sum()`

Returns the sum of all the die

#### `count()`

Returns a dictionary where all the keys are the unique dice face (`dice.value`) and all the values are the number of occurances of each dice face.

#### `sort(reverse=True)`

Sorts the dice in place, highest to lowest unless reverse is `False`, default is `True`