from dicecup import DiceCup

class PyZhee(DiceCup):

    def __init__(self):
        super().__init__('5d6')

    def find_kinds(self, num):
        """
        Finds X of a Kind and puts them in a list of tuples (value, number_of_value)
        """
        count = self.count()
        results = []
        for key in count:
            if count[key] >= num:
                results.append((key, count[key]))
        return results

    def of_a_kind(self, num):
        """
        Checks if a kind is present or not, of a specific number, returns true if the kind is present
        """
        if len(self.find_kinds(num)) != 0:
            return True
        return False

    def full_house(self):
        """
        Returns true if a full house is present
        """
        three_of_kind = self.find_kinds(3)
        two_of_kind = self.find_kinds(2)
        if len(three_of_kind) != 0 and len(two_of_kind) != 0:
            for three in three_of_kind:
                for two in two_of_kind:
                    if three[0] != two[0]:
                        return True
        return False

    def straight(self):
        """
        Finds the length of a straight
        """
        self.sort()
        i = 0; j = 1; count = 0
        while j < len(self.dice):
            if abs(self.dice[i] - self.dice[j]) == 1:
                count += 1
            i += 1
            j += 1
        return count

    def sm_straight(self):
        """
        returns true if small straight
        """
        return self.straight() >= 3

    def lg_straight(self):
        """
        returns true if large straight
        """
        return self.straight() == 4

    def odd_man_out(self):
        """
        Return the one die that doesn't fit a small straight
        """
        if self.lg_straight or not self.sm_straight:
            # if there isn't a straight, or if there's a large straight, there's no odd man
            return None
        else:
            # if the value is in the middle, it has to be a duplicate
            if self.of_a_kind(2):
                return self.find_kinds(2)[0]
            # if the value isn't a duplicate, it's either the first or last value
            else:
                dice = self.dice.copy()
                dice.sort()
                if abs(dice[0] - dice[1]) != 1:
                    return dice[0]
                else:
                    return dice[4]
