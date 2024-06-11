def scl(bb: int, n1, n2, n3):
    if bb % 10 == 1:
        return n1
    elif (bb % 10 >= 2) and (bb % 10 <= 4):
        return n2
    elif (5 <= (bb % 10) <= 20) or bb % 10 == 0:
        return n3