from copy import deepcopy

from code.algorithms.breadth_first import BreadthFirst
from code.classes.game import Game


class BreadthFirst_adjusted(BreadthFirst):

    def __init__(self, game, boards, max_depth, step):
        self.boards = boards
        self.game = deepcopy(game)
        self.max_depth = max_depth
        self.step = step

        # initiate archive
        self.state_keys = [] #self.game.give_board()
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
                if len(new_state_data[1]) > (self.max_depth + self.step):
                    print(new_state_data[1])
                    break

            game_node = Game(self.game.board_size, self.game.game_number, new_state_data) # VOOR DIE BOARD SIZE EVEN EEN APARTE METHOD MAKEN IN GAME
            

            if count % 100 == 0:
                print(f"ROW:{(len(new_state_data[1]) - self.step)}")
                # print(f"number of keys: {len(self.state_keys)}")

            for car in self.cars: 
                for i in self.move_range:
                    # check if the move is valid/possible
                    if game_node.valid_move(car, i):
                        if game_node.get_moves() and [car,-i] == game_node.get_moves()[-1]:
                            continue
                        self.build_child(game_node, car, i)

                    if self.best_solution != None:                          # DIT IN APARTE FUNCTIE DOEN ZODAT JE NIET 3X HOEFT TE BREAKEN
                        print(f"found a solution: {self.best_solution}")
                        break

                if self.best_solution != None:
                    break
            
            if self.best_solution != None:
                break

        print(f"Number of keys when breaking out of breadthfirst: {len(self.state_keys)}")

    def build_child(self, game_node, car, move):
        """
        Creates all possible child-states and adds them to the list of states
        """
 
        # make a new state
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        # move the car
        new_node.move(car, move)
        # print([new_node.give_board()])
        # check if it is a solution
        if [new_node.give_board()] in self.boards:
            print("FOUND ONE!!!")
            # print(self.boards)
            # print([new_node.give_board()])

            self.best_solution = new_node.get_moves()
            self.index = self.boards.index([new_node.give_board()])  
        else:
            self.add_to_archive(new_node)

    def give_solution(self):
        return self.best_solution, self.index

class Breadthfirst_improver:
    
    def __init__(self, game):
        self.game = deepcopy(game)
        self.moves_file = "data/output_files/breadthfirst_improver_6_52moves54.csv"  # DIT KUNNEN WE EVENTUEEL ALS IMPUT DOEN IN COMMAND LINE
        self.max_depth = 6                                                   # DIT OOK
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
        self.game_boards.append([game_for_boards.give_board()])

        for move in self.solution:
            game_for_boards.move(*move)
            self.game_boards.append([game_for_boards.give_board()])

        self.game_boards_total_length = len(self.game_boards)
        self.game_boards = self.game_boards[self.max_depth + 2:]
        # print(self.game_boards)
        # check for every board if there is a route to one of the other boards that is more than the max depth away
        step_counter = 0

        while True:
            print(f"game board length: {len(self.game_boards)}")
            if not self.game_boards:
                break
            
            print(f"Checking board {step_counter + 1}")

            print(f"moves van game waarmee ie de breadthfirst ingaat: {self.game.get_moves()}")
            breadthfirst = BreadthFirst_adjusted(self.game, self.game_boards, self.max_depth, step_counter)

            partial_solution, index = breadthfirst.give_solution()
            print(partial_solution)
            print(index)
            if partial_solution:
                # replace that piece of code in the solution
                print(self.solution)
                self.solution[: (self.game_boards_total_length - len(self.game_boards) + index)] = partial_solution
                print(self.solution)
                break

            self.game_boards.pop(0)
            self.game.move(*self.solution[step_counter])
            step_counter += 1

    def get_command(self):
        command_list = self.solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"