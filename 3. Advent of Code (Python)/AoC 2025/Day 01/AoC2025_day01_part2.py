#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


### initial position
pos = 50
prev_pos = 50
count_zeros = 0

# for each instruction
for instr in input_array:

    # get direction +/- 1 (R=1, L=-1), and move size from instruction
    direction = (instr[0] == "R")*2 - 1
    move_size = int(instr[1:])

    # right away count any moves > 100 since they obviously cross 0, then apply modulo to limit move to < 100
    count_zeros += move_size//100
    move_size %= 100

    pos += move_size*direction

    # since move is limited to < 100, no edge case of starting on a 0 will touching another 0
    # with edge case removed, anything outside 1-99 touched a 0
    if prev_pos != 0 and pos <= 0 or pos >= 100:
        count_zeros += 1
    
    
    pos %= 100  
    prev_pos = pos
 
# END for instr


## print solution
print(count_zeros)