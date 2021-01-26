from copy import deepcopy

from code.algorithms.breadth_first import BreadthFirst
from code.classes.game import Game

# constants
MAX_DEPTH = 4


class BreadthFirst_adjusted(BreadthFirst):
    """
        This class inherits from the breadthfirst algorithm and contains some
        adjustments to make it suitable to improve an existing solution with
        the Breadthfirst_improver algorithm. Parameters: game(Game object), 
        boards(list of strings), max_depth(int), step_counter(int).
    """

    def __init__(self, game, boards, max_depth, step_counter):
        self.boards = boards
        self.game = deepcopy(game)
        self.max_depth = max_depth
        self.step_counter = step_counter

        # initialise archive
        self.state_keys = []
        self.states = {}
        self.add_to_archive(game)
        
        # game variables
        self.move_range = self.game.get_move_range()
        self.cars = game.get_cars()

        self.index = None
        self.best_solution = None

        self.create_solution(self.max_depth, self.step_counter)


    def build_child(self, game_node, car, move):
        """
            Performs a move and checks if it results in a board that is present
            further on in the solution. If it is, the solution and the index of 
            the board further on in the solution are saved. 
            Parameters: game_node(Game object), car(string), move(int).
        """
        # make new state and perform move
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        new_node.move(car, move)
        
        # check if shorter solution has been found
        if [new_node.give_board()] in self.boards:
            self.best_solution = new_node.get_moves()
            self.index = self.boards.index([new_node.give_board()])  
        else:
            self.add_to_archive(new_node)

    def give_solution(self):
        return self.best_solution, self.index

class Breadthfirst_improver:
    
    def __init__(self, game):
        self.game = deepcopy(game)
        self.solution_file = "data/output_files/breadthfirst_improver_7_240moves243.csv"
        self.max_depth = MAX_DEPTH

        # load solution that needs to be improved from file
        self.solution = self.load_solution(self.solution_file)

        # make a list of game states
        self.game_boards, self.game_boards_total_length = self.make_game_states_list(self.game, self.solution, self.max_depth)

        # improve the solution using breadthfirst
        self.run_improver()

    def load_solution(self, solution_file):
        with open(solution_file) as f:
            next(f)
            solution = []

            for line in f:
                move = line[:-1].split(",")
                solution.append(move)
        
        return solution

    def make_game_states_list(self, game, solution, depth):
        # make a list with all the states of the board
        game_for_boards = deepcopy(game)
        game_boards = []
        game_boards.append([game_for_boards.give_board()])

        for move in solution:
            game_for_boards.move(*move)
            game_boards.append([game_for_boards.give_board()])

        game_boards_total_length = len(game_boards)
        game_boards = game_boards[depth + 2:]

        return game_boards, game_boards_total_length

    def run_improver(self):
        # check for every board if there is a route to one of the other boards that is more than the max depth away

        step_counter = 0

        while self.game_boards:
            
            print(f"Checking board {step_counter + 1}")
            print(f"Remaining game board length: {len(self.game_boards)}")

            # run breadthfirst
            breadthfirst = BreadthFirst_adjusted(self.game, self.game_boards, self.max_depth, step_counter)
            partial_solution, index = breadthfirst.give_solution()

            if partial_solution:
                # replace that piece of code in the solution
                self.solution[: (self.game_boards_total_length - len(self.game_boards) + index)] = partial_solution
                return

            self.game_boards.pop(0)
            self.game.move(*self.solution[step_counter])
            step_counter += 1

    def get_command(self):
        command_list = self.solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"