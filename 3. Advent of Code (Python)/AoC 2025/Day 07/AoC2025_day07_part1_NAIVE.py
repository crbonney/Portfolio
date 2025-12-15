#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

# create empty set to store laser positions and add initial position
laser_set = set()
laser_set.add(input_array[0].index("S"))

# for each row in the laser tree... 
# 1. generate list of splitters, 
# 2. compare against set of lasers
# 3. update count and laser set if match
num_splits = 0
for row in input_array:

    # locations of spliters in this row
    splitter_list = [i for (i, char) in enumerate(row) if char == "^"]

    # loop through set of lasers, use a copy to allow for editting set mid loop
    for laser in laser_set.copy():
        # if laser lands on a splitter, split it and add to count
        if laser in splitter_list:
            laser_set.add(laser+1)
            laser_set.add(laser-1)
            laser_set.remove(laser)
            num_splits += 1

    # END for splitters in row
# END for rows

# print solution
print(num_splits)
