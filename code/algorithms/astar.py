from copy import deepcopy

from .random_repeater import Random_repeater
from code.classes.game import Game

class AStar:
    def __init__(self, board_size, game_number):
        # self.board_size = 
        self.solution = Random_repeater(board_size, game_number).get_game()
        self.board = Game(board_size, game_number)

        self.move_range = list(range(- self.board.board_size + 2, self.board.board_size - 1))
        self.move_range.remove(0)
        self.cars = [x for x in self.board.car_ids]

        self.best_solution = None

        self.score = self.calculate_score(self.board)

        self.shorten_solution()


    def calculate_score(self, game):
        score = 0

        for car in self.solution.cars:
            if self.solution.cars[car].orientation == "H":
                score += abs(self.solution.cars[car].col - game.cars[car].col)
            else:
                score += abs(self.solution.cars[car].row - game.cars[car].row)

        return score
    
    def shorten_solution(self):
        while True:
            for car in self.cars: 
                for i in self.move_range:
                    # check if the move is valid/possible
                    if self.board.valid_move(car, i):
                        new_board = Game(self.solution.board_size, self.solution.game_number, deepcopy(self.get_node_data(self.board)))
                        new_board.move(car, i)
                        
                        if new_board.game_won():
                            self.best_solution = new_board.get_moves()
                            print(len(self.best_solution))
                        elif self.calculate_score(new_board) < self.score:
                            self.board.move(car, i)
                        else:
                            continue

                if self.best_solution != None:
                    break


    def get_node_data(self, game_node):
        """
        Make list with car, orientation, column, row and length and moves
        """
        info = []
        for car_id in game_node.cars:
            car = game_node.cars[car_id]
            info.append(f"{car.id},{car.orientation},{car.col},{car.row},{car.length}")

        moves = game_node.get_moves()
        return [info, moves]

    
    def get_command(self):
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"