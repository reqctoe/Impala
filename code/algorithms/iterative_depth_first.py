from copy import deepcopy

from code.classes.game import Game


class Iterative_depth_first():
    """
    This class is used to implement a depth first search with iterative deepening 
    that tries to find a solution for the Rushhour game using a recursive function.
    """

    def __init__(self, game):

        # initialise game variables
        game_info = game.get_game_info()
        self.board_size = game_info["board_size"]
        self.game_number = game_info["game_number"]
        self.board_file = f"data/gameboards/Rushhour{self.board_size}x{self.board_size}_{self.game_number}.csv"  
        self.cars = game.get_cars()
        self.moves = game.get_move_range()
        self.depth = 0

        self.run_iterative_depth_first()


    def run_iterative_depth_first(self):
        """
        Repeats a depth first search with increasing depth until an answer
        for the Rushhour game has been found.
        """
        while True:
            self.best_solution = self.run_depth_first([], self.depth)

            if self.best_solution:
                break

            self.depth += 1
            print(f"Depth: {self.depth}")


    def run_depth_first(self, parent_moves, depth):
        """
        Creates children unless the maximum depth has been reached. If 
        maxumum depth has been reached, checks for all possible moves if 
        it solves the game. Parameters: parent_moves(list of moves),
        depth(int).
        """
        if depth > 0:
            depth -= 1

            # create children for all possible moves
            for car in self.cars:
                for move in self.moves:
                    new_parent_moves = deepcopy(parent_moves)
                    new_parent_moves.append([car, move])
                    best_solution = self.run_depth_first(new_parent_moves, depth)

                    if best_solution:
                        return best_solution

        # if maximum depth reached, check all possible moves
        for car in self.cars:
            for move in self.moves:
                # add current move to parent moves
                try_moves = deepcopy(parent_moves)
                try_moves.append([car, move])
                self.game = Game(self.board_size, self.game_number)

                # perform all moves and check for solution
                for try_move in try_moves:
                    if not self.game.valid_move(*try_move):
                        break
                    self.game.move(*try_move)
                
                    if self.game.game_won():
                        return try_moves

        return False



    def get_command(self):
        """
        Returns the command to move a car
        """
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"


