#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


### initial position
pos = 50
prev_pos = 50
count_zeros = 0
last_rotation_landed_on_zero = False

# for each instruction
for instr in input_array:
    # get direction +/- 1 (R=1, L=-1)
    direction = (instr[0] == "R")*2 - 1
        

    num_rots = int(instr[1:])
    
    for _ in range(num_rots):
        pos += direction
        if pos%100 == 0:
            count_zeros += 1

 
# END for instr


## print solution
print(count_zeros)