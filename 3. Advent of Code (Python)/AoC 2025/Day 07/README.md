
# [2025, Day 7](https://adventofcode.com/2025/day/7)


## Input:

Grid of `.` and `^` with a single `S` on the top line as a starting point. Ex:

```
....S....
.........
....^..^.
.........
.^.^.^...
.........
```

## Part 1:
A beam originates traveling straight down from the `S`, splitting left and right whenever it touches a `^`. Calculate the number of splits that occur. In the example above, there are 3 splits (one in row 3, then each split beam is split an additional time in row 5).



## Part 2:
Using the same beam as before, calculate the number of possible paths the beam could take to travel the bottom. In the example, there are 4 paths (left or right at the first `^` in row 3, then for each splitter in row 5, there are two more options for a total of 4: LL, LR, RL, RR).
