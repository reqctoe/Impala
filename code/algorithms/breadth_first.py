from copy import deepcopy

from code.classes.game import Game

class BreadthFirst:
    
    def __init__(self, game):
        self.game = deepcopy(game)

        # initiate archive
        self.state_keys = [self.game.give_board()]
        self.states = {}
        self.add_to_archive(game)
        
        # game variables
        self.move_range = list(range(- self.game.board_size + 2, self.game.board_size - 1))
        self.move_range.remove(0)
        self.cars = [x for x in game.car_ids]

        self.best_solution = None

        self.create_solution()


    def add_to_archive(self, game):
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


    def get_next_state(self):
        key = self.state_keys.pop(0)
        
        # print(f"Queue length: {len(self.state_keys)}")
        state_data = self.states[key]
        self.states[key] = ""

        return state_data


    def build_child(self, game_node, car, move):
        """
        Creates all possible child-states and adds them to the list of states
        """
 
        # make a new state
        new_node = Game(self.game.board_size, self.game.game_number, deepcopy(self.get_node_data(game_node)))
        # move the car
        new_node.move(car, move)

        # check if it is a solution
        if new_node.game_won():
            self.best_solution = new_node.get_moves()
            print(len(self.best_solution))
        else:
            self.add_to_archive(new_node)


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