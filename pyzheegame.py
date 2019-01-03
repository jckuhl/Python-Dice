from operator import itemgetter
from pyzheecup import PyZhee
from pyzheefuncs import loop_multi_player

def game(players):
    """
    Starts, runs and ends the game
    """
    num_players = len(players)
    pyzhee = PyZhee()
    pyzhee.roll_all()
    print('Welcome to PyZhee!')
    index = 0
    turns = num_players * 13
    while turns > 0:
        loop_multi_player(players, index, pyzhee)
        index += 1
        if index >= num_players:
            index = 0
        turns -= 1
    print('Game over!')
    final_scores = [(player.name, player.score_board.get_grand_total()) for player in players]
    for score in final_scores:
        print(f'{score[0]}: scored {score[1]}')
    winner = max(final_scores, key=itemgetter(1))
    print(f'{winner[0]} wins with a score of {winner[1]}')
    print(f'Thank you for playing!')