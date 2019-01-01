from scoreboard import ScoreBoard

class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn = False
        self.values = []
        self.score_board = ScoreBoard()

    def play_turn(self, dicecup):
        if self.turn:
            self.values = dicecup.roll_all()
            return self.values
        return None

    def set_value(self, num, index):
        self.values[index] = num