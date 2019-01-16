def get_max(dic):
    if len(dic.items()) == 0:
        return None
    max_value = list(dic.items())[0][1]
    max_item = None
    for elem in dic:
        if dic[elem] > max_value:
            max_value = dic[elem]
            max_item = elem
    return { max_item: max_value }