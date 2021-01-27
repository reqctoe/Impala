
from copy import deepcopy

from code.classes.game import Game


class Breadth_first_recursive():
    
    def __init__(self, game):

        # get game variables
        game_info = game.get_game_info()
        self.board_size = game_info["board_size"]
        self.game_number = game_info["game_number"]
        self.board_file = f"data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv"  
        self.cars = game.get_cars()
        self.moves = game.get_move_range()

        self.depth = 0

        while True:
            self.best_solution = self.run_children([], self.depth)
            if self.best_solution:
                break
            self.depth += 1
            print(f"Depth: {self.depth}")


    def run_children(self, parent_moves, depth):

        if depth < 1:
            for car in self.cars:
                for move in self.moves:
                    try_moves = deepcopy(parent_moves)
                    try_moves.append([car, move])
                    # print(try_moves)
                    self.game = Game(self.board_size, self.game_number)

                    for try_move in try_moves:
                        if not self.game.valid_move(*try_move):
                            break
                        self.game.move(*try_move)
                    
                        if self.game.game_won():
                            return try_moves
            return False

        depth -= 1

        for car in self.cars:
            for move in self.moves:
                new_parent_moves = deepcopy(parent_moves)
                new_parent_moves.append([car, move])
                best_solution = self.run_children(new_parent_moves, depth)

                if best_solution:
                    return best_solution


    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"


