import copy

class BreadthFirst:
    
    def __init__(self, game):
        self.game = copy.deepcopy(game)

        # make copy of the current game
        self.states = [copy.deepcopy(self.game)]

        self.best_solution = None

        # self.cars = []
        # self.board_file = f"data/gameboards/Rushhour{board_size}x{board_size}_{game_number}.csv"

        # self.load_cars(self.board_file)


    # def load_cars(self, board_file):
    #     """
    #     Loads all the car id's from the board file into a list. 
    #     Needs the board file name (string) as parameter.
    #     """

        
        
    #     with open(board_file) as f:
    #         # skip header and read each car into list
    #         next(f)

    #         for line in f:
    #             car_line = line.split(",")
    #             self.cars.append(car_line[0])


    def get_next_state(self):
        return self.states.pop(0)

    def build_children(self, game_state, car):
        """
        Creates all possible child-states and adds them to the list of states
        """
        # 
        for car in self.game.car_ids: # weet niet precies in welke variabele dit gaat zitten
            for i in [-1,1]:
                # check if the move is valid/possible
                if game_state.valid_move(car, i):
                    # make a new state
                    new_game_state = copy.deepcopy(game_state)
                    # move the car
                    new_game_state.move(car, i)
                    # check if it is a solution
                    if new_game_state.won():
                        self.best_solution = new_game_state
                    else:
                        self.states.append(new_game_state)
    
    def run(self): # moet dit in main.py of in de init worden aangeroepen?
        """
        Zolang je self.states lijst niet leeg is:
            RIJ 1:
                pak de begin state 
            RIJ 2-n:
                pak het eerste element uit state lijst
                check of solution
                nee:
                    gooi in build_children
                .....               
        """

        while self.states:
            new_state = self.get_next_state()

            build_children(new_state)

            if self.best_solution != None:
                return self.best_solution.get_moves # moet ie returnen?

    def get_command(self):
        command_list = self.best_solution.get_moves # is get moves nodig?
        car, move = command_list[0:2]
        return f"{car},{move}"
        
            