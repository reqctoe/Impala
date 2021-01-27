from copy import deepcopy

from code.classes.game import Game

class BreadthFirst:
    """
    This class is used to implement the breadth first algorithm to solve
    the Rushhour game. Parameter: game(Game object)
    """
    
    def __init__(self, game):
        self.game = deepcopy(game)

        # initialise archive
        self.state_keys = []
        self.states = {}
        self.add_to_archive(game)
        
        # game variables
        self.move_range = self.game.get_move_range()
        self.cars = self.game.get_cars()

        # step counter for breadthfirst improver
        self.step_counter = 0

        # run breadthfirst
        self.best_solution = None
        self.create_solution()


    def add_to_archive(self, game):
        """
        Adds the game to the queue(self.state_keys) and the archive(self.states).
        Parameter: game(Game object).
        """
        if game.give_board() not in self.states:
            self.state_keys.append(game.give_board())
            self.states[game.give_board()] = self.get_node_data(game)


    def create_solution(self): 
        """
        
        """
        count = 0

        while self.state_keys:
            count += 1
            new_state_data = self.get_next_state()

            # # stop if max depth has been reached
            # if max_depth:
            #     if len(new_state_data[1]) > (max_depth + step_counter):
            #         break

            # create game node
            game_node = Game(self.game.board_size, self.game.game_number, new_state_data)


            # regularly print current depth
            if count % 100 == 0:
                # if used in breadthfirst improver, subtract number of steps taken
                print(f"Depth:{(len(new_state_data[1]) - self.step_counter)}")

            # check all cars
            for car in self.cars:
                # skip last car that has been moved
                if game_node.get_moves() and car == game_node.get_moves()[-1][0]:
                    continue
                # check all possible moves the car can make
                for i in self.move_range:
                    # if move is valid, build child
                    if game_node.valid_move(car, i):
                        self.build_child(game_node, car, i)

                    # if a solution has been found, stop algorithm
                    if self.best_solution != None:
                        return
        
    
    def get_next_state(self):
        """
        Get the string representation of a game from the queue and 
        return the data to create a new game object for it.
        """
        key = self.state_keys.pop(0)
        
        # print(f"Queue length: {len(self.state_keys)}")
        state_data = self.states[key]
        self.states[key] = ""

        return state_data


    def build_child(self, game_node, car, move):
        """
        Performs a move and checks whether that move solves the game.
        If it does, it saves the move. Parameters: game_node(Game object),
        car(string), move(int).
        """
 
        # make a new state and perform move
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        new_node.move(car, move)

        # check if it is solution
        if new_node.game_won():
            self.best_solution = new_node.get_moves()
        else:
            self.add_to_archive(new_node)


    def get_node_data(self, game_node):
        """
        Make list with information needed to create a game. 
        Parameter: game_node(Game object)
        """
        info = []
        for car_id in game_node.cars:
            car = game_node.cars[car_id]
            info.append(f"{car.id},{car.orientation},{car.col},{car.row},{car.length}")

        moves = game_node.get_moves()
        return [info, moves]        


    def get_command(self):
        """
        Gives a move in a command string appropriate for the main function.
        """
        command_list = self.best_solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"