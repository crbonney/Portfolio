# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:49:44 2024

@author: crbon
"""

import numpy as np 


### PARSE INPUT
input_file = open("input1", "r")
input_array = input_file.read().splitlines()

## finds the index of the blank line in the input
height = input_array.index("")
width  = len(input_array[0])

## split input array into the separate components
warehouse_map = input_array[0:height]
instruction_list = input_array[height+1:]

move_string = "".join(instruction_list)


warehouse_map = [[0 if x=="." else x for x in warehouse_map[i]] for i in range(height)]
warehouse_map = [[1 if x=="O" else x for x in warehouse_map[i]] for i in range(height)]
warehouse_map = [[5 if x=="@" else x for x in warehouse_map[i]] for i in range(height)]
warehouse_map = [[120 if x=="#" else x for x in warehouse_map[i]] for i in range(height)]


np_map = np.array(warehouse_map,dtype=np.int8)


def consecutive_start(arr):
    streak = 1
    arr_len = len(arr)
    while streak < arr_len and arr[streak-1]+1 == arr[streak]:
        streak += 1
    return streak



for i in range(len(move_string)):

    # print("move " + str(i) + ": " + move_string[i])
    

    (pos_row,pos_col) = np.where(np_map == 5)
    pos_row = pos_row[0]
    pos_col = pos_col[0]

    
    # move up
    if move_string[i] == "^":
        move_array = np_map[pos_row::-1,pos_col]
        pos_array = (np.where(move_array > 0)[0])
        streak = consecutive_start(pos_array)
        # no walls in the way
        if sum(move_array[:streak]) < 120:
            move_dist = streak
            np_map[pos_row:pos_row-streak-1:-1,pos_col] = np.insert(move_array[:streak],0,0)
        # wall in the way
        else:
            move_dist = 0

    # move right
    if move_string[i] == ">":
        move_array = np_map[pos_row,pos_col:]
        pos_array = (np.where(move_array > 0)[0])
        streak = consecutive_start(pos_array)
        # no walls in the way
        if sum(move_array[:streak]) < 120:
            move_dist = streak
            np_map[pos_row,pos_col:pos_col+streak+1] = np.insert(move_array[:streak],0,0)
        # wall in the way
        else:
            move_dist = 0

    # move down
    if move_string[i] == "v":
        move_array = np_map[pos_row:,pos_col]
        pos_array = (np.where(move_array > 0)[0])
        streak = consecutive_start(pos_array)
        # no walls in the way
        if sum(move_array[:streak]) < 120:
            move_dist = streak
            np_map[pos_row:pos_row+streak+1,pos_col] = np.insert(move_array[:streak],0,0)
        # wall in the way
        else:
            move_dist = 0

    # move left
    if move_string[i] == "<":
        move_array = np_map[pos_row,pos_col::-1]
        pos_array = (np.where(move_array > 0)[0])
        streak = consecutive_start(pos_array)
        # no walls in the way
        if sum(move_array[:streak]) < 120:
            move_dist = streak
            np_map[pos_row,pos_col:pos_col-streak-1:-1] = np.insert(move_array[:streak],0,0)
        # wall in the way
        else:
            move_dist = 0        

## END FOR move_string

box_pos = (np.where(np_map == 1))
        
solution = np.sum(box_pos[0]*100 + box_pos[1])
print(solution)