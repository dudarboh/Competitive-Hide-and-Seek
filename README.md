# Competitive Hide and Seek (Fully Written-Out Challenge!)

- Theme: Puzzle/algorithm
- Difficulty: Medium
- Time Estimate: 1-2 weeks

Feel free to read the submission on [github](https://github.com/dudarboh/Competitive-Hide-and-Seek#) with pictures and code.

## Concept

You and your friend are playing hide & seek.
You both randomly spawn in 2D grid-like room. The room has randomized walls that obstruct vision.
If you are a seeker, your goal is to write an algorithm to catch the hider with the least steps possible.
If you are a hider, your goal is to write an algorithm to delay the catching as much as possible.
You can choose whether you want to play as a seeker, or a hider. You can submit for both sides if you like.

## Winners

All submitted algorithms for seekers and hiders will compete against each other on a predefined hidden test set of random maps and starting locations.

The algorithm's performance is evaluated as an average across all games number of steps to catch the hider.

Therefore are two sets of gold/silver/bronze winners.
Three for the best seeker algorithm. Three for the best hider algorithm.

## Game Rules

### Map

The map is a 2D grid of 20x20 (always same size) cells.
Each map has randomly placed walls of different shapes.
The walls always cover approximately 25% of the map and in such a way that there are no inaccesible cells.

### Movement

Both players are only allowed to move left, right, up, down if there is no wall in front of the movement and they don't go out of bounds of the map.

The speed of the seeker is double the hider, to make catching possible.
I.e. the seeker moves every step/iteration, while the hider moves only every *second* step.

On the second step, the seeker has the priority, i.e., the hider two distances away is always being caught if the seeker moves towards the hider.

### Spawn Locations

The spawn of a seeker is uniformly random on the entire map.
The spawn of a hider is uniformly random on the furtherst quadrant from the seeker spawn to make close-distant spawns less likely.

The spawn at the distance closer than three is forbidden, as it is an automatic win for the seeker.
The players spawn only in the "non-wall" (empty) cells.

### Vision

The players have vision of each other if there are no walls crossing the line connecting the two players.
Once the players have vision of each other, they get the precise coordinates of their opponents.

### Beginning of the game

At the beginning of the game both players are given the full knowledge of the map and the starting locations of both the seeker and the hider.

### End of the game

When the seeker's location becomes the hider's location the game is over and the number of the steps it took is the score for both algorithms.

To avoid games taking too long to finish, there are two other constraints:
1. The maximum number of steps is 10 x map_size = 4000. If the hider is not caught within 4000 steps hider considered a winner with the highest score of 4000.
2. If the game lasts more than 5 minutes on the testing computer, the game is aborted and the player who thought for the least time is considered a winner with the best possible score (1 for the seeker, 4000 for the hider).

## Code Details

### Map Generation

```bash
python3 map.py
```

## Submission Rules

### Language

The challange is on solving the puzzle.
Thus, the specific programming language is not strictly required to solve it.
However, the final submission should be in python to make testing and table of records possible.
The language of submission is chosen to be python, as it has the easiest syntax and is more likely to be picked up by novices and potentially can catch wider audience rather than requiring the solution in C++ or JS.

### AI usage

You are allowed to use AI tools as well as LLM generated content any way you like.
However, if you use the AI directly for the help with the solution, you are required to disclaim this, and explain which parts are your own, which are the the AI's. If the AI's contribution to the algorithm solution found substaintial, your solution will be marked with the *(AI)* to indicate AI usage in the table of records.

### Exploits

The challange is on writing the algorithm, thus hacks and exploits are not the primary goal of this challange and the code is not indended to be exploitable.
However, exploits are not forbidden. If you manage to find an exploit you are welcome to do so and write your submission. Your entry in the table of records will be marked with *(exploit)* though, to indicate out-of-the-box solution.

However, if the code has a bug and allows very trivial exploits that can be abused by many, they are likely to be patched live :)

### Performance Requirements

There are no CPU, memory requirements.
There is a mild, but obligatory time requirement of the game time to be within 1 minute on the testing machine.
If the game exceeds 1 minute execution time, the algorithm contributing most to the execution time will be disqualified!
This is to avoid any algorithms that think infinitely about the next step.
Please make sure your algorithms are not stuck in the infinite loops and don't break games!

### Code guidlines

