
# [2025, Day 10](https://adventofcode.com/2025/day/10)
*Difficult to describe succinctly, see [the puzzle's page](https://adventofcode.com/2025/day/10) for a full description of the puzzle.*

## Input:
A line-seperated set of data, with each row containing 3 sets of information: 
- a binary number (encoded as `.` for 0 and `#` for 1) contained within square brackets, 
- a set of sets contained within parentheses ("buttons"), containing numbers between 0 and the length of the binary number minus 1, 
- and a set of integers, matching the length of the binary number contained within curly braces: 

EX:

```
[.#.] (0) (1,2) (1) (2) {4,5,9}
[...#] (2,3) (0) (1) (1,2) {1,2,4,4}
```


## Part 1:
Letting each "button" in the second set of each row toggle those digits of the binary number, for each row determine the fewest number of button presses required to reach the binary number in the square brackets.
Ex: 
- for the first row, only one button is needed: (1) toggles the center giving `.#.`
- for the second row, we need 3: (3,2) -> `..##`; (1,2) -> `.#.#`; (1) -> `...#`


## Part 2:
For each row, determine the fewest number of button presses to toggle each term exactly `n` times where `n` is the number encoded in the curly brackets for each term. 
Ex: 
- for the first row, we would press (1,2) 5 times {0,5,5}; then (0) 4 times {4,5,5}; then (2) 4 times {4,5,9})
- for the second row, we would press (2,3) 4 times {0,0,4,4}; (0) 1 time {1,0,4,4}; and (1) 2 times {1,2,4,4}