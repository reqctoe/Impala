
from copy import deepcopy

from code.classes.game import Game


class Test_alg_2():
    
    def __init__(self, board_size, game_number):
        self.board_size = int(board_size)
        self.game_number = game_number
        self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"
    
        self.cars = []
        self.load_cars(self.board_file)

        self.moves = self.create_move_list()

        self.best_solution = self.run_children([]) # IETS MET DEPTH TOEVOEGEN OM ER EEN BREADTH FIRST VAN TE MAKEN

    def run_children(self, parent_moves):
        for car in self.cars:
            for move in self.moves:
                try_moves = deepcopy(parent_moves)
                try_moves.append([car, move])
                print(try_moves)
                self.game = Game(self.board_size, self.game_number)

                for try_move in try_moves:
                    if not self.game.valid_move(*try_move):
                        break
                    self.game.move(*try_move)
                
                    if self.game.game_won():
                        return try_moves

        for car in self.cars:
            for move in self.moves:
                new_parent_moves = parent_moves
                new_parent_moves.append([car, move])
                best_solution = self.run_children(new_parent_moves)

                if best_solution:
                    return best_solution



    def load_cars(self, board_file):    # DIT KAN MISSCHIEN STRAKS WEG OMDAT HET AL IN GAME.PY STAAT
        """
        Loads all the car id's from the board file into a list. 
        Needs the board file name (string) as parameter.
        """

        with open(board_file) as f:
            # skip header and read each car into list
            next(f)

            for line in f:
                car_line = line.split(",")
                self.cars.append(car_line[0])

    def create_move_list(self):

        moves = list(range(-(self.board_size - 2), self.board_size - 1))
        moves.remove(0)

        return moves

    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"


