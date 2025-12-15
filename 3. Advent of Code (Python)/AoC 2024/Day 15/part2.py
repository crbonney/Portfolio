# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:49:44 2024

@author: crbon
"""

# import re
import numpy as np


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

## finds the index of the blank line in the input
height = input_array.index("")
width  = len(input_array[0])

## split input array into the separate components
warehouse_map = input_array[0:height]
instruction_list = input_array[height+1:]

move_string = "".join(instruction_list)


# converts map to integers and widens it
# sum([[a,b] for x in arr],[]) replaces every element in arr with a,b
warehouse_map = [sum([[0,0] if x=="." else [x] for x in warehouse_map[i]], []) for i in range(height)]
warehouse_map = [sum([[1,2] if x=="O" else [x] for x in warehouse_map[i]], []) for i in range(height)]
warehouse_map = [sum([[5,0] if x=="@" else [x] for x in warehouse_map[i]], []) for i in range(height)]
warehouse_map = [sum([[120,120] if x=="#" else [x] for x in warehouse_map[i]], []) for i in range(height)]

np_map = np.array(warehouse_map,dtype=np.int8)

# initialize robot position
(pos_row,pos_col) = np.where(np_map == 5)
pos_row = pos_row[0]
pos_col = pos_col[0]


#works for horizontal movement still
def consecutive_start(arr):
    streak = 1
    arr_len = len(arr)
    while streak < arr_len and arr[streak-1]+1 == arr[streak]:
        streak += 1
    return streak


# cases to handle:
# 1. single box (links 1,2 and recurses)
# 2. offset box (discontinues part of tree, and links new box pair)
# 3. wall (breaks chain and cancels movement)

def get_vertical_box_tree_recursive(y_move, prev_row_idx, prev_col_set):

    # print(prev_row_idx,prev_col_set)
       
    next_col_set = set() # use set to automatically handle potential duplicates
    # print(sum([[i,i+1] if prev_row_idx != pos_row else [i] for i in prev_col_set],[]))
    # makes iterable for each box's left and right side, and accounting for the starting robot only being 1 wide
    for y in sum([[i,i+1] if prev_row_idx != pos_row else [i] for i in prev_col_set],[]):
        # only add the left half of the box to the stack
        if np_map[prev_row_idx+y_move][y] == 1:
            # print("left box - STACK")
            next_col_set.add(y)
        elif np_map[prev_row_idx+y_move][y] == 2:
            # print("right box - STACK")
            next_col_set.add(y-1) # stacks left side of box, right side will be automatically included
        elif np_map[prev_row_idx+y_move][y] == 120:
            # print("wall - MOVE FAIL")
            return False # returns false for invalid movement
        elif np_map[prev_row_idx+y_move][y] == 0:
            # print("empty - CONTINUE")
            continue
    #END FOR

    # print(next_col_set)
    # empty set, no more boxes to push -> move is valid, end recursion
    if (len(next_col_set) == 0):
        # print("empty set, ending recursion")
        # if no boxes were pushed, only move robot
        if prev_row_idx == pos_row:
            # print("moving robot only")
            np_map[pos_row+y_move][pos_col] = 5
            np_map[pos_row][pos_col] = 0
            return True # returns true for valid movement
            
        for y in prev_col_set:
            # print("moving box", prev_row_idx,y)
            # add boxes to new location
            np_map[prev_row_idx+y_move][y] = 1
            np_map[prev_row_idx+y_move][y+1] = 2
            # remove boxes from old location
            np_map[prev_row_idx][y] = 0
            np_map[prev_row_idx][y+1] = 0
        #END FOR

        return True # returns true for valid movement
    #END IF

    
    valid_move = get_vertical_box_tree_recursive(y_move, prev_row_idx+y_move, next_col_set)
    
    # if move is invalid, pass it back up the chain
    if (valid_move == False):
        return False
    # else perform the move and pass it back up the chain
    else:
        # robot move
        if prev_row_idx == pos_row:
            # print("moving robot only")
            np_map[pos_row+y_move][pos_col] = 5
            np_map[pos_row][pos_col] = 0
            return True # returns true for valid movement
        
        for y in prev_col_set:
            # print("moving box", prev_row_idx,y)
            # add boxes to new location
            np_map[prev_row_idx+y_move][y] = 1
            np_map[prev_row_idx+y_move][y+1] = 2
            # remove boxes from old location
            np_map[prev_row_idx][y] = 0
            np_map[prev_row_idx][y+1] = 0
        return True
    #END ELSE
#END def get_vertical_box_tree_recursive

def get_horizontal_box_tree_recursive(x_move,prev_pos_col):
    
    # if space is wall, return invalid movement
    if np_map[pos_row][prev_pos_col+x_move] == 120:
        # print("hit wall")
        return False
    
    # if space is empty, move box and retrun valid movement
    if np_map[pos_row][prev_pos_col+x_move] == 0:
        # print("empty space - move valid, moving")
        np_map[pos_row][prev_pos_col+x_move] = np_map[pos_row][prev_pos_col]
        np_map[pos_row][prev_pos_col] = 0
        return True
    else:
        # print("hit box, continuing")
        valid_move = get_horizontal_box_tree_recursive(x_move,prev_pos_col+x_move)
    
    # continue invalid move up the chain
    if valid_move == False:
        return False
    # perform valid move and continue up the chain
    else:
        np_map[pos_row][prev_pos_col+x_move] = np_map[pos_row][prev_pos_col]
        np_map[pos_row][prev_pos_col] = 0
        return True
#END def get_horizontal_box_tree_recursive    


# loop through all moves in the move string
for i in range(len(move_string)):

    # print("move " + str(i) + ": " + move_string[i])

    # move up
    if move_string[i] == "^":

        # recursive function to check/perform move up
        valid_move = get_vertical_box_tree_recursive(-1, pos_row, {pos_col})
        pos_row = pos_row - 1*valid_move # if move is valid, update robot position


    # move down
    if move_string[i] == "v":

        # recursive function to check/perform move down
        valid_move = get_vertical_box_tree_recursive(1, pos_row, {pos_col})
        pos_row = pos_row + 1*valid_move


    # move right
    if move_string[i] == ">":
        # recursive function to check/perform move right
        valid_move = get_horizontal_box_tree_recursive(1, pos_col)
        pos_col = pos_col + 1*valid_move


    # move left
    if move_string[i] == "<":
        # recursive function to check/perform move left
        valid_move = get_horizontal_box_tree_recursive(-1, pos_col)
        pos_col = pos_col - 1*valid_move

## END FOR move_string

box_pos = (np.where(np_map == 1)) # gets location of all the left sides of boxes for solution's "GPS" calculation

solution = np.sum(box_pos[0]*100 + box_pos[1])
print("GPS solution:", solution)
