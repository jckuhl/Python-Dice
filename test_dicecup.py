import unittest

from dicecup import DiceCup
from random import Random

class TestDiceCup(unittest.TestCase):

    dicecup = DiceCup('5d6')

    def setUp(self):
        global random
        random = Random(123)

    def test_dicecup_init(self):
        """ A 5d6 should make five six sided dice """
        self.assertEqual(len(self.dicecup.dice), 5)
        for die in self.dicecup.dice:
            self.assertEqual(die.sides, 6)

        # Lets assert on a different size of dice, 3d20
        dicecup = DiceCup('3d20')
        self.assertEqual(len(dicecup.dice), 3)
        for die in dicecup.dice:
            self.assertEqual(die.sides, 20)

    def test_dice_roll(self):
        """ A 5d6 roll should net 5 values """
        self.assertEqual(len(self.dicecup.values), 0)
        self.dicecup.roll_all()
        self.assertEqual(len(self.dicecup.values), 5)
    
    def test_set_dice(self):
        self.dicecup.set_values([1,2,3,4,5])
        self.assertListEqual(self.dicecup.set_values, [1,2,3,4,5])
    
