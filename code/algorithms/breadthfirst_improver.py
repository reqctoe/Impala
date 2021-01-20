


class Breadthfirst_improver:
    
    def __init__(self, game):
        self.game = game
        self.moves_file = "data/output_files/random_loopcutter_7_263moves"
        self.solution = []

        with open(self.moves_file) as f:
            next(f)
            for line in f:
                self.solution.append(line.split(","))
        
        print(self.solution)

    def get_command(self):
        command_list = self.solution.pop(0)
        car, move = command_list[0:2]
        return f"{car},{move}"