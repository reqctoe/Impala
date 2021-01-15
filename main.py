from code.algorithms.baseline_algorithm import Baseline
from code.algorithms.test_alg_1 import Test_alg_1
from code.algorithms.test_alg_2 import Test_alg_2
from code.algorithms.breadth_first import BreadthFirst

from code.classes.game import Game

import csv
from sys import argv


if __name__ == "__main__":

    # check if command line arguments are given
    if len(argv) != 3:
        print("Usage: python main.py [game_number] [board_size]")
        exit(1)
    
    # check game number
    if int(argv[1]) not in range(1, 8):
        print("Invalid game number")
        exit(1)

    # check board size
    if int(argv[2]) not in [6, 9, 12]:
        print("Invalid board size")
        exit(1)

    # load game
    game_number, board_size = argv[1], argv[2]
    game = Game(board_size, game_number)

    # # load algorithm
    # algorithm = BreadthFirst(game)
    
    # ask user what algorithm they want to run
    print("Type the number of the algorithm that you want to run")
    print("1 baseline: Fills in random numbers")
    print("2 test alg 1: tries to fill in random numbers and r")
    print("3 test alg 2: breadth first without heuristics")
    print("4 breadth first: breadth first with dictionary heuristic")

    # keep asking for input until an algorithm is loaded
    while True:
        algorithm_number = input("> ")

        if algorithm_number == 1:
            algorithm = Baseline(board_size, game_number)
        elif algorithm_number == 2:
            algorithm = Test_alg_1(board_size, game_number)
        elif algorithm_number == 3:
            algorithm = Test_alg_2(board_size, game_number)
        elif algorithm_number == 4:
            algorithm = BreadthFirst(game)
        else:
            print("Invalid algorithm number")
            continue

        break

    # initiate move registration and move counters
    command_list = ""
    command_count = 0
    valid_command_count = 0

    # initiate output file
    with open('data/output_files/output.csv', 'w', newline ='') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["car", "move"])
        
    # print welcome message and initial game board
    print("Enter a move in the folowing format:\n[car_id],[move]\n" +
            "when you want to move left or up, enter a negative number.")

    print(" " + game.give_board())
    
    """
    deze doet nu nog allemaal checks die niet nodig zijn aangezien hij 
    alleen solutions aangereikt krijgt 
    """

    # ask algorithm for input
    while True:
        command_string = algorithm.get_command()
        command_count += 1
        
        # check if move is valid
        command = command_string.split(",")
        
        # if not game.valid_move(*command):
        #     continue
        # count valid move
        valid_command_count += 1
        
        # update output string and perform move
        command_list += f"{command_string}\n"
        game.move(*command)
       
        # exit when game is won
        if game.game_won():
            # print final gameboard state and total number of input and valid moves
            print(" "+game.give_board())
            print(command_count)
            print(valid_command_count)
            print("Congratulations, you have won the game!")

            # write all valid moves to output file
            with open('data/output_files/output.csv', 'a') as outputfile:
                outputfile.write(command_list)

            exit(0)
        
