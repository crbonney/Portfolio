# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 19:30:06 2024

@author: crbon
"""

import numpy as np 
### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


height = len(input_array)
width = len(input_array[0])


num_array = [[1 if x=="." else x for x in input_array[i]] for i in range(height)]
num_array = [[2 if x=="^" else x for x in num_array[i]] for i in range(height)]
num_array = [[-1 if x=="#" else x for x in num_array[i]] for i in range(height)]




## find starting position
np_array = np.array(num_array,dtype=np.int64)
start_pos = np.where(np_array == 2)
[pos_row,pos_col] = [start_pos[0][0], start_pos[1][0]]

# make a copy for later use in part 2
original_array = np_array.copy()
original_array[start_pos] = 1 # remove starting location

# [up,down,left,right]
DIRECTIONS = [2,3,5,7]
# init facing up
direction = 2

on_map = True
i = 0
while on_map:
    
    # multiplier for prime number path direction detection
    direction = DIRECTIONS[i%4]
    # find which direction guard is moving +/-1 for [row,col]
    move_dir = [(direction == 2)*-1 + (direction == 5)*1, (direction == 3)*1 + (direction == 7)*-1]

    # array of possible moves based on current position and direction
    move_array = np_array[pos_row + move_dir[0] : ((pos_row+1) if move_dir[0] == 0 else None) : move_dir[0]+(move_dir[0]==0), 
                          pos_col + move_dir[1] : ((pos_col+1) if move_dir[1] == 0 else None) : move_dir[1]+(move_dir[1]==0)]

    # how far it is possible to move before hitting an obstacle 
    move_delta = np.where(move_array == -1)
    # if np.where returned empty, there were no obstacles and we reached the end of the map
    if np.size(move_delta) == 0:
        # move as far as possible and trigger flag to exit loop
        move_delta = np.size(move_array)
        on_map = False
    # else we can move to obstacle
    else:
        move_delta = move_delta[move_dir[0] == 0][0]

    # multiply positions moved by direction prime [2,3,5,7] = [up,right,down,left]
    np_array[pos_row + move_dir[0]: pos_row + move_dir[0]*(move_delta+1) + (move_dir[0] == 0) : move_dir[0]+(move_dir[0]==0), 
             pos_col + move_dir[1]: pos_col + move_dir[1]*(move_delta+1) + (move_dir[1] == 0) : move_dir[1]+(move_dir[1]==0)] *= direction
    
    # calculate new position
    pos_row += move_delta*move_dir[0]
    pos_col += move_delta*move_dir[1]
    i+=1
    if (i%500 == 0):
        print("i = ", i)

## END WHILE on_map

print("~~~~~~~~~~~~~~~PART 1 COMPLETE~~~~~~~~~~~~~~~~~~~")

move_locations = np.where(np_array > 1)
move_rows = move_locations[0]
move_cols = move_locations[1]


placable_obstacles = 0

for s in range(len(move_rows)):
    
    if (s%500 == 0):
        print("progress: s = ", s)
    
    move_directions = np_array[move_rows[s],move_cols[s]]
    
    placed_obstacle = False
    
    # print("testing ", [move_rows[s],move_cols[s]])
    
    for d in range(len(DIRECTIONS)):
        
        if placed_obstacle:
            break
        
        # # didn't pass through this square in the given direction, skip
        if move_directions%DIRECTIONS[d] != 0:
            continue
        
        i=d # set starting direction for test
        # i = 0

        # multiplier for prime number path direction detection
        start_dir = DIRECTIONS[d%4]

        # find which direction guard is moving +/-1 for [row,col]
        move_dir = [(start_dir == 2)*-1 + (start_dir == 5)*1, (start_dir == 3)*1 + (start_dir == 7)*-1]

        # set starting position for test 1 before current location
        # start_pos = [move_rows[s]-move_dir[0],move_cols[s]-move_dir[1]]
        # [pos_row,pos_col] = start_pos

        [pos_row,pos_col] = [start_pos[0][0], start_pos[1][0]] # ORIGINAL START

        ## create test map, and place the test obstacle
        test_map = original_array.copy()
        test_map[move_rows[s],move_cols[s]] = -1
        
        i+=1
        i=0

        ## TEST IF GUARD LEAVES MAP BEFORE RETURNING TO PREVIOUSLY CALCULATED PATH
        on_map = True
        while on_map:
            
            
            # multiplier for prime number path direction detection
            direction = DIRECTIONS[i%4]
            # find which direction guard is moving +/-1 for [row,col]
            move_dir = [(direction == 2)*-1 + (direction == 5)*1, (direction == 3)*1 + (direction == 7)*-1]
        
            # array of possible moves based on current position and direction
            move_array = test_map[pos_row + move_dir[0] : ((pos_row+1) if move_dir[0] == 0 else None) : move_dir[0]+(move_dir[0]==0), 
                                  pos_col + move_dir[1] : ((pos_col+1) if move_dir[1] == 0 else None) : move_dir[1]+(move_dir[1]==0)]
        
            # how far it is possible to move before hitting an obstacle 
            move_delta = np.where(move_array == -1)
            # if np.where returned empty, there were no obstacles and we reached the end of the map
            if np.size(move_delta) == 0:
                # move as far as possible and trigger flag to exit loop
                move_delta = np.size(move_array)
                on_map = False
            # else we can move to obstacle
            else:
                move_delta = move_delta[move_dir[0] == 0][0]
        
            # multiply positions moved by direction prime [2,3,5,7] = [up,right,down,left]
            test_map[pos_row + move_dir[0]: pos_row + move_dir[0]*(move_delta+1) + (move_dir[0] == 0) : move_dir[0]+(move_dir[0]==0), 
                     pos_col + move_dir[1]: pos_col + move_dir[1]*(move_delta+1) + (move_dir[1] == 0) : move_dir[1]+(move_dir[1]==0)] *= direction
            
            # calculate new position
            pos_row += move_delta*move_dir[0]
            pos_col += move_delta*move_dir[1]
            
            
            # if have crossed a square twice
            if test_map[pos_row,pos_col] % direction**2 == 0 and not placed_obstacle:
            # if i > 1000:
                placable_obstacles += 1
                placed_obstacle = True
                # print("placed obstacle")
                break
            i += 1


        ## WHILE on_map TEST END
        
    ## FOR EACH DIRECTION END
    
## FOR EACH SQUARE TRAVERSED IN PART 1 END
        
## PART 1 SOLUTION
total_moves = np.count_nonzero(np_array > 1)
print("total moves: ", total_moves)

## PART 2 SOLUTION
print("placable obstacles: ", placable_obstacles)


### PART 2: determine where obstructions could cause an infinite loop
## GOAL: find all locations where the path intersects itself *AND* the direction of the intersected path is 1 larger than the current path
## IDEA: track path with *prime numbers* for each direction [2,3,5,7], when crossing a path, multiply by the prime number. Then, when crossing a path (index with value > 1), check if it is divisible by the next prime number
## Set obstructions to "1" and empty spaces to "0"

#### INVALID - there are obstacles that can be placed in locations not on the intersections that send the route back onto a path

### NEW IDEA:
## Still use prime numbers, BUT instead of checking at the end, 
## check each row/col perpendicular to and (right of/touching) the direction of travel to see if it contains the correct prime

## This SHOULD work but...
# 1. needs to check each section of path individually - otherwise we might undercount if two options are available on a single route
# during each step in the path, compute each possible added obstacle individually
# 2. needs to check if the possible obstruction is reachable (ie there isnt an existing obstruction already in the way)
#    - check if theres an index of -1 before the index of the [prime] 