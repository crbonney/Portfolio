#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### PARSE INPUT
input_file = open("input1", "r")
input_array = input_file.read().splitlines()


### initial position
pos = 50
count_zeros = 0

# for each instruction
for instr in input_array:
    # get direction +/- 1 (R=1, L=-1)
    direction = (instr[0] == "R")*2 - 1
    pos = (pos + int(instr[1:])*direction) % 100
    if pos == 0:
        count_zeros+=1
    
# END for instr

## print solution
print(count_zeros)