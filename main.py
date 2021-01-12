from code.algorithms.baseline_algorithm import Baseline
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

    # load algorythm
    baseline = Baseline(board_size, game_number)

    # initiate move registration and move counter
    command_list = ""
    command_count = 0

    # initiate output file
    with open('data/output_files/output.csv', 'w', newline ='') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["car", "move"])
        
    # print welcome message and initial game board
    print("Enter a move in the folowing format:\n[car_id],[move]\n" +
            "when you want to move left or up, enter a negative number.")

    print(" " + game.give_board())
    
    # ask algorythm for imput
    while True:
        command_string = baseline.get_command()
        command_count += 1
        
        # check if move is valid
        command = command_string.split(",")

        if not game.valid_move(*command):
            continue
        
        # update output string and perform move
        command_list += f"{command_string}\n"
        game.move(*command)

        # exit when game is won
        if game.game_won():
            # print final gameboard state and total number of imput moves
            print(" "+game.give_board())
            print(command_count)
            print("Congratulations, you have won the game!")

            # write all valid moves to output file
            with open('data/output_files/output.csv', 'a') as outputfile:
                outputfile.write(command_list)

            exit(0)
        
