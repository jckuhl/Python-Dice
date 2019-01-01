
class ScoreBoard:

    def __init__(self):
        self.score = {
            "ones": None,
            "twos": None,
            "threes": None,
            "fours": None,
            "fives": None,
            "sixes": None,
            "totalupper": None,
            "threeofakind": None,
            "fourofakind": None,
            "fullhouse": None,
            "smstraight": None,
            "lgstraight": None,
            "yahtzee": None,
            "yahtzeebonus": None,
            "totallower": None,
            "grandtotal": None
        }
    
    def find_kinds(self, num, count):
        """
        Finds X of a Kind and puts them in a list of tuples (value, number_of_value)
        Count is a dictionary coming from a DiceCup object that has a count of all the values
        """
        results = []
        for key in count:
            if count[key] >= num:
                results.append((key, count[key]))
        return results

    def of_a_kind(self, num, count):
        """
        Checks if a kind is present or not, of a specific number, returns true if the kind is present
        """
        if len(self.find_kinds(num, count)) != 0:
            return True
        return False

    def one_pair(self, count):
        """
        Returns true if a single pair is present
        """
        return len(self.find_kinds(2, count)) >= 1

    def two_pair(self, count):
        """
        Returns true if a two pair or a 4 of a kind is present
        """
        return len(self.find_kinds(2, count)) >= 2 or len(self.find_kinds(4, count)) >= 1

    def get_highest_die(self, count):
        """
        Returns the highest value die
        """
        keys = list(map(lambda key: int(key), count.keys))
        return keys.sort()[0]

    def full_house(self, count):
        """
        Returns true if a full house is present
        """
        three_of_kind = self.find_kinds(3, count)
        two_of_kind = self.find_kinds(2, count)
        if len(three_of_kind) != 0 and len(two_of_kind) != 0:
            for three in three_of_kind:
                for two in two_of_kind:
                    if three[0] != two[0]:
                        return True
        return False

    def straight(self, dicecup):
        """
        Finds the length of a straight
        """
        dicecup.sort()
        i = 0; j = 1; count = 0
        while j < len(dicecup.dice):
            if abs(dicecup.dice[i] - dicecup.dice[j]) == 1:
                count += 1
            i += 1
            j += 1
        return count

    def sm_straight(self, dicecup):
        """
        returns true if small straight
        """
        return self.straight(dicecup) >= 3

    def lg_straight(self, dicecup):
        """
        returns true if small straight
        """
        return self.straight(dicecup) == 4

    def count_numbers(self, number, count):
        """
        Counts the number of numbers in the dice
        """
        number = str(number)
        if number in count.keys:
            return count[number]
        else:
            return 0

    def total_lower(self):
        keys = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
        subtotal = 0
        for key in keys:
            subtotal += self.score[key]
        if subtotal >= 63:
            subtotal += 35
        return subtotal


    def total_upper(self):
        keys = ['threeofakind', 'fourofakind', 'fullhouse', 'smstraight', 'lgstraight', 'yahtzee']
        subtotal = 0
        for key in keys:
            subtotal += self.score[key]
        if self.score['yahtzeebonus'] is not None:
            subtotal += 100 * self.score['yahtzeebonus']
        return subtotal

    def grandtotal(self):
        return self.score['totalupper'] + self.score['totallower']