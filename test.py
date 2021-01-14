

def create_move_list():
    moves = list(range(-(6 - 2), 6 - 1)).remove(0)
    moves.remove(0)

    return moves

moves = create_move_list()
print(moves)