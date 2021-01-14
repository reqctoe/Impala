

class Test_alg_2():
    
    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"