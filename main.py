

from code.classes.game import Game 
from code.algorithms.baseline_algorithm import Baseline

import csv
from sys import argv

if __name__ == "__main__":

    # check if command lina arguments are given
    if len(argv) != 3:
        print("Usage: python main.py [game_number] [board_dimention]")
        exit(1)
    
    # check game number
    if int(argv[1]) not in range(8):
        print("Invalid game number")
        exit(1)

    # check board dimension
    if int(argv[2]) not in [6, 9, 12]:
        print("Invalid board dimension")
        exit(1)

    # load game
    game_number, board_dimension = argv[1], argv[2]
    game = Game(board_dimension, game_number)
    baseline = Baseline(board_dimension, game_number)
    command_list = ""
    command_count = 0

    # initiate output file
    with open('data/output_files/output.csv', 'w', newline ='') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["car", "move"])
        

    print("Enter a move in the folowing format:\n[car_id],[move]\n" +
            "when you want to move left or up, enter a negative number.")

    print(" "+game.give_board())
    
    # prompt user for commands
    while True:
        command_string = baseline.get_command()
        command_count += 1

        # if "," not in command:
        #     print("Invalid command. Enter a move in the folowing format:\n[car_id],[move]")
        #     continue
        
        command = command_string.split(",")
        
        # check if move is valid
        if not game.valid_move(*command):
            # print("Invalid move")
            continue
        
        command_list += f"{command_string}\n"

        # perform move an print current board
        game.move(*command)
        # print(" "+game.give_board())

        # exit when game is won
        if game.game_won():
            print(" "+game.give_board())
            print(command_count)
            print("Congratulations, you have won the game!")
            with open('data/output_files/output.csv', 'a') as outputfile:
                # writer = csv.writer(outputfile)
                # writer.writerow(command_list)
                outputfile.write(command_list)
            exit(0)
        
