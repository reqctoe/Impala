# Rush Hour
Rush Hour is based on the logic game with the same name. You have a board, either 6x6, 9x9 or 12x12, filled with cars, length 2, and trucks, length 3. These cars can only move either horizontally or vertically, depending on their orientation. The goal is to move car X to the right side of the board, where the exit is, in as few moves as possible. 

## Getting started
### Requirements

This program is written in Python 3.8.5. No additional installations are necessary to run the code. 

### Usage

All algorithms can be run by executing the following command:

```
python3 main.py
```

The terminal will then inquire whether you want to generate a random board or use a pre-generated board followed by a list of algorithms to run. Further instructions are provided by the terminal.

### Structure

The list below describes the most important folders from the project:

- **/code**: contains all code for this project
  - **/code/advanced**: contains the algorithm for generating new game boards 
  - **/code/algorithms**: contains all algorithms for solving the game
  - **/code/classes**: contains three classes for the game representation
- **/data**: contains all data files for generating games as well as solutions
  - **/data/gameboards**: contains data files for starting positions of the games
  - **/data/output_files**: contains all solutions, ordered by algorithm 
- **/docs**: contains files displaying the data structure of the representation of a Rush Hour game and the advanced assignment

## Algorithms
### 1 - Random
This algorithm tries to solve the game using random moves. It continuously moves a random car a random number of steps until car X is at the right side of the board and the game is won. Only valid moves are executed. 

We used this algorithm to create our baseline. Because it is completely random, the resulting solutions are often very high.

### 2 - Iterative depth first
This algorithm was a bit of an experiment and was abandoned quite early on because the breadth first algorithm showed more promise and had an easier way to implement heuristics because it uses an archive. 

The idea of this algorithm is that it searches all possible moves depth first, starting with a maximum depth of 1 and if no solution is found it tries a maximum depth of 2 and so on. 

Because no heuristics are applied, the runtime is too long to produce any results. 

### 3 - Breadth first
This algorithm uses the breadth first search method, which means it uses a queue to first try all possible moves with one move then all possible moves with two moves etc. The upside of this algorithm is that when it finds a solution, it will always be the optimal solution. The downside is that the runtime and memory usage for larger boards will become too large to find a solution.

The pruning we did for this algorithm is removing all the invalid moves before they had to be checked. More importantly, we use an archive to save all the states (game board configurations). We use this to make sure that states that are already checked or already in the queue are not put in the queue again.

To further reduce the runtime and memory usage, we save just enough information as value into the archive dictionary to reproduce the game, which is a lot faster than making a deepcopy of the game and saving it in the dictionary. And to save even more memory, we replace this value by an empty string once the state has been checked. 

With this algorithm we found solutions for the first 4 games and because of the nature of this algorithm they are also the optimal solution. For the larger boards, no results have been found.

### 4 - Depth first with breadth first heuristics





### 5 - Random Repeater
The Random Repeater algorithm is an addition to the Random algorithm. It also executes random moves until the game is won. This is repeated x times, specified by the user. If a shorter solution is found, it will save that. If the number of moves gets higher than the current best solution, the algorithm will stop and go to the next iteration. 

This algorithm gives results that are a lot better than those generated with Random, but, unless you get really lucky, they are still quite far from the best or optimal solution.

### 6 - Random Loopcutter
The Random Loopcutter algorithm is an addition to Random Repeater. It uses Random Repeater to generate a solution. After this it iterates through all the board configurations/states. If a certain state is found multiple times in the solution, it will cut all moves between the first time and the last time that specific state is found. 

The results generated with this algorithm strongly depend on the solution found with Random Repeater. Sometimes it can bring down the amount of moves a lot, and sometimes it cannot cut any moves. Generally though, the results are better than those of Random Repeater, but still not near as good as the (optimal) results of breadth first. 

### 7 - A*
This algorithm uses our random loop cutter to generate a board in a winning state. This board is then used for the heuristics of A*. 

Costs consist of the amount of moves performed and the displacement of all cars compared to their winning state counterparts. This score is then used to calculate the “optimal” next move. 

However, this is not guaranteed to be the optimal move as it might be necessary to move cars to and from their final location multiple times. 
Therefore, the algorithm is likely to get stuck in a loop of moves that the algorithm deems the optimal next state without 

### 8 - Breadthfirst improver
This algorithm uses the breadth first algorithm we wrote earlier to improve upon a solution that has been found with another algorithm (such as random loopcutter). It applies the breadth first algorithm with a specified depth to each state that the initial solution passes through. The breadth first algorithm searches all possible states with the moves it can do within its maximum depth and compares these states with states further on in the initial solution. If a state matches, it means that a shorter path to that state has been found. The algorithm replaces the longer solution with the shorter solution and returns it.

This algorithm turned out to be very effective for improving the larger game boards that could not be solved with the standard breadth first algorithm.

## Advanced
When running the code, you also get the option to generate your own game board. All boards generated with this are solvable. However, especially the 6x6 boards are really easy most of the time and can often be solved in 10 moves or less.

Our insights into what makes a Rush Hour game harder or easier can be found in **/docs/advanced**.

## Authors
- Iza Bosch
- Eline van de Lagemaat
- Joris Oud