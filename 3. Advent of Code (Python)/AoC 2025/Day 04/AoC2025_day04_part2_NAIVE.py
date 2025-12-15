#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

num_rows = len(input_array)
num_cols = len(input_array[0])

num_movable = 0
prev_moved = -1
num_iterations = 0 

# iteratively check for new paper rolls to move until a full iteration with none removed
while prev_moved != num_movable:

    num_iterations += 1
    # store current number of moved rolls to check for changes at end of loop
    prev_moved = num_movable

    # for all rows, columns
    for r in range(num_rows):
        for c in range(num_cols):
    
            # skip if entry isn't a roll of paper
            if input_array[r][c] != "@": continue
    
            num_adjacent = 0
            for i in range(-1,2):
                # skip if out of bounds
                if r+i < 0 or r+i == num_rows: continue
                for j in range(-1,2):
                    # skip if out of bounds
                    if c+j < 0 or c+j == num_cols: continue
                    
                    # +1 adjacent if entry is an @
                    if input_array[r+i][c+j] == "@":
                        num_adjacent+=1
            
            # END for adjacent
            
            # print(r,c, num_adjacent)    
            # count++ if less than 4 adjacent paper rolls (note, it counts itself, so -1)
            if num_adjacent < 5: 
                num_movable += 1
                input_array[r] = input_array[r][:c] + "." + input_array[r][c+1:]

    
        # END for cols
    # END for rows
# END while changes have been made
    
# print solution
print(num_movable, "removable rolls. found in", num_iterations, "iterations")