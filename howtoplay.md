# How to Play PyZhee

PyZhee is a Python implementation of the Hasbro game Yatzhee and follows the same rules.  It is also a proof of concept and a rough draft for a later version with a graphical user interface.

PyZhee can be played with multiple people or against the computer.

## Installation and Running

Download all the files using `git clone`:

    https://github.com/jckuhl/Python-Dice.git

`cd` into the directory and run `python3 pyzhee.py`

Alternatively you can download the executable from [here]() (**TODO:** link not implemented)

The program takes player names as an argument.  If it recieves no arguments, it starts a game against the computer, and names the player `Player 1`.

If it recieves one argument, it starts a game against the computer and names the player the given argument

If it recieves two or more arguments, it starts the game in multiplayer mode

Singleplayer
``` bash
python3 pyzhee.py
python3 pyzhee.py Mike
```

Multiplayer
```bash
python3 pyzhee.py Jim Pam Mike Dwight Oscar
```

Exiting the game prematurely at any time can be done by typing `quit`, `exit`, `q`, `x` or `e` whenever you're offered an input prompt.  Note that your progress on the current game will be irrevocably lost.

## Gameplay

PyZhee is a turn based game.  Each player can roll upto three times.  The objective is to find specific patterns in the dice.  The game lasts 13 rounds (the amount of rounds it takes to fill the score sheet) for each player.  The player with the most points at the ened wins.

During your turn you have upto three rolls (including your initial roll.)  If you don't like what you see, when prompted, enter an `A` to reroll all your dice or enter the number of each dice you want to roll.

For example if you see this:

    Here are the current values:
    1: [6], 2: [6], 3: [1], 4: [2], 5: [1]
    Enter the number for each dice you'd like to reroll, or 'A' to reroll all:

If you want to reroll the third, fourth and fifth die, just enter `345`

When you either run out of rolls in your turn or get a combination that you like, you can enter your score into the desired field.  Simply type the field exactly as you see it in the display when you're prompted.

> All inputs are case insensitive

Once you've entered a value into a field on the scoreboard, you cannot enter a new value.  You **must** enter a score into a field, even if your only choice is to enter a score into a field where it counts for nothing.

The only exception to this clause is the Yatzhee Bonus which can be reused every time you get a Yatzhee (five in a row) after your first Yatzhee.

## Scoring

| Field | Definition |Score |
|-------|------------|-------------------------------|
| Ones  | All the ones| Add all the ones in your hand|
| Twos  | All the twos| Add all the twos in your hand|
| Threes  | All the threes| Add all threes ones in your hand|
| Fours  | All the fours| Add all the fours in your hand|
| Fives  | All the fives| Add all the fives in your hand|
| Sixes  | All the sixes| Add all the sixes in your hand|
| Bonus*  | Applied if the above are worth 63 or more | 35 points|
| 3 of a Kind | 3 or more of any value | Sum of all the dice |
| 4 of a Kind | 4 or more of any value | Sum of all the dice |
| Full House | A pair and a 3 of a kind | 25 points |
| Small Straight | Four in a row | 30 points |
| Large Straight | Five in a row | 40 points |
| Yatzhee | Five of a kind | 50 points |
| Yatzhee Bonus | Applied for every Yatzhee after the first | 100 points per bonus |

> *The bonus is calculated automatically