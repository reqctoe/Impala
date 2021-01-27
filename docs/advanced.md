# Advanced

There are a few things that can make a Rush Hour game easier or more difficult.

When considering horizontal vs vertical cars, both categories individually do not obstruct car X from moving to the exit. It is only when both vertical and horizontal cars are present that complications occur. 
Therefore, a larger amount of cars in the game does not necessarily mean it is more difficult to solve. An example of this is game 2 and 3. Both are 6x6 boards; game 2 has 12 cars and 1 truck, while game 3 has 6 cars and 3 trucks. However, game 2 can be solved in 15 moves, while game 3 needs 33 moves. 

This gap in difficulty can also be attributed to the amount of cars vs. trucks. Since trucks are larger, they obstruct significantly more movement than cars do. They probably have the biggest influence on difficulty for a 6x6 board as they cover half the board length.

What also likely affects the difficulty of a game is the ratio between horizontal and vertical cars. As mentioned before, only when they are both present do they form an obstruction. This means that in order to make a game more complex, a 1:1 ratio of the two is ideal. 
When considering games 1 and 2, their H:V ratios are 7:5 and 8:4 respectively. The amount of cars and trucks in both games are exactly the same, but in line with the aforementioned, game 1 can be solved in 21 moves and game 2 in 15. 

This pattern can also be recognized when comparing the 9x9 boards as can be seen in the table below:

| Game  | H:V ratio | Solution length  |
| ----- |-----------| -----------------|
| 4     | 10:11     | 27               |
| 5     | 11:12     | 27               |
| 6     | 14:11     | 22               |

The solutions for games 5 and 6 are not guaranteed optimal since they were not produced by the breadth first algorithm alone, but they are likely a quite good approximation.
Even though game 5 has more cars than game 4, increasing the size of the state space so significantly that breadth first can no longer solve game 5, its solution is not longer.
This points to the correlation between H:V ratio and difficulty. Game 6 in turn has even more cars than does game 5 but its solution is shorter than both previous games whose H:V ratio was closer to 1.