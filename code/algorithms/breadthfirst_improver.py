from copy import deepcopy

from code.algorithms.breadth_first import BreadthFirst
from code.classes.game import Game


class BreadthFirst_adjusted(BreadthFirst):

    def __init__(self, game, boards, max_depth):
        self.boards = boards
        self.game = deepcopy(game)
        self.max_depth = max_depth

        # initiate archive
        self.state_keys = [self.game.give_board()]
        self.states = {}
        self.add_to_archive(game)
        
        # game variables
        self.move_range = list(range(- self.game.board_size + 2, self.game.board_size - 1))
        self.move_range.remove(0)
        self.cars = [x for x in game.car_ids]

        self.index = None
        self.best_solution = None

        self.create_solution()

    def create_solution(self): 
        """
              
        """
        count = 0

        while self.state_keys:
            count += 1
            new_state_data = self.get_next_state()
            # print(new_state_data)

         
            # stop if max depth has been reached
            if count > 100:
                if len(new_state_data[1]) > self.max_depth:
                    break

            game_node = Game(self.game.board_size, self.game.game_number, new_state_data)
            

            if count % 100 == 0:
                print(f"ROW:{len(new_state_data[1])}")

            for car in self.cars: 
                for i in self.move_range:
                    # check if the move is valid/possible
                    if game_node.valid_move(car, i):
                        if game_node.get_moves() and [car,-i] == game_node.get_moves()[-1]:
                            break
                        self.build_child(game_node, car, i)

                if self.best_solution != None:
                    break

    def build_child(self, game_node, car, move):
        """
        Creates all possible child-states and adds them to the list of states
        """
 
        # make a new state
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        # move the car
        new_node.move(car, move)

        # check if it is a solution
        if new_node.give_board in self.boards:
            self.best_solution = new_node.get_moves()
            self.index = self.boards.index(new_node.give_board)  
        else:
            self.add_to_archive(new_node)

    def give_solution(self):
        return self.best_solution, self.index

class Breadthfirst_improver:
    
    def __init__(self, game):
        self.game = deepcopy(game)
        self.moves_file = "data/output_files/random_loopcutter_6_67moves.csv"  # DIT KUNNEN WE EVENTUEEL ALS IMPUT DOEN IN COMMAND LINE
        self.max_depth = 6                                                      # DIT OOK
        self.solution = []

        # load solution from file
        with open(self.moves_file) as f:
            next(f)

            for line in f:
                move = line[:-1].split(",")
                self.solution.append(move)
        
        # make a list with all the states of the board
        game_for_boards = deepcopy(self.game)
        self.game_boards = []
        self.game_boards.append(game_for_boards.give_board())

        for move in self.solution:
            game_for_boards.move(*move)
            self.game_boards.append(game_for_boards.give_board())

        self.gameboards = self.game_boards[self.max_depth + 1:]

        # check for every board if there is a route to one of the other boards that is more than the max depth away
        step_counter = 0

        while True:
            if not self.game_boards:
                break
            
            print(f"Checking board {step_counter + 1}")

            breadthfirst = BreadthFirst_adjusted(self.game, self.gameboards, self.max_depth)

            partial_solution, index = breadthfirst.give_solution()

            if partial_solution:
                # replace that piece of code in the solution
                self.solution[step_counter: index - 1] = partial_solution

                break

            step_counter += 1

    def get_command(self):
        command_list = self.solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"