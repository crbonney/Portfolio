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
np_array = np.array(num_array,dtype=np.int8)
(pos_row,pos_col) = np.where(np_array == 2)
pos_row = pos_row[0]
pos_col = pos_col[0]

# [up,down,left,right]
DIRECTIONS = [2,3,5,7]
# init facing up
direction = 2

on_map = True
i = 0
while on_map:
    
    direction = DIRECTIONS[i%4]
    # find which direction guard is moving +/-1 for [row,col]
    move_dir = [(direction == 2)*-1 + (direction == 5)*1, (direction == 3)*1 + (direction == 7)*-1]

    move_array = np_array[pos_row + move_dir[0] : ((pos_row+1) if move_dir[0] == 0 else None) : move_dir[0]+(move_dir[0]==0), 
                          pos_col + move_dir[1] : ((pos_col+1) if move_dir[1] == 0 else None) : move_dir[1]+(move_dir[1]==0)]

    move_delta = np.where(move_array == -1)
    if np.size(move_delta) == 0:
        move_delta = np.size(move_array)
        on_map = False
    else:
        move_delta = move_delta[move_dir[0] == 0][0]

    # print(move_delta)
    
    np_array[pos_row + move_dir[0]: pos_row + move_dir[0]*(move_delta+1) + (move_dir[0] == 0) : move_dir[0]+(move_dir[0]==0), 
             pos_col + move_dir[1]: pos_col + move_dir[1]*(move_delta+1) + (move_dir[1] == 0) : move_dir[1]+(move_dir[1]==0)] *= direction
    
    pos_row += move_delta*move_dir[0]
    pos_col += move_delta*move_dir[1]
    i+=1


total_moves = np.count_nonzero(np_array > 1)
print("total moves: ", total_moves)




### PART 2: determine where obstructions could cause an infinite loop
## GOAL: find all locations where the path intersects itself *AND* the direction of the intersected path is 1 larger than the current path
## IDEA: track path with *prime numbers* for each direction [2,3,5,7], when crossing a path, multiply by the prime number. Then, when crossing a path (index with value > 1), check if it is divisible by the next prime number
## Set obstructions to "1" and empty spaces to "0"

## RESULT: np.count_nonzero(np_array > 1)