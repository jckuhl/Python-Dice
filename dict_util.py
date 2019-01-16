def get_max(dic):
    """
    Given a dictionary of keys with related values, return the entry with the highest value
    Example: A scoreboard of players and their scores.
    """
    if len(dic.items()) == 0:
        return None
    max_item, max_value = list(dic.items())[0]
    for elem in dic:
        if dic[elem] > max_value:
            max_value = dic[elem]
            max_item = elem
    return { max_item: max_value }

def get_min(dic):
    """
    Given a dictionary of keys with related values, return the entry with the highest value
    Example: A scoreboard of players and their scores.
    """
    if len(dic.items()) == 0:
        return None
    min_item, min_value = list(dic.items())[0]
    for elem in dic:
        if dic[elem] < min_value:
            min_value = dic[elem]
            min_item = elem
    return { min_item: min_value }

if __name__ == '__main__':
    actors = {
        'Robert Duvall': 92,
        'Alan Alda': 91,
        'Mel Brooks': 93
    }
    print(get_max(actors))
    print(get_min(actors))
