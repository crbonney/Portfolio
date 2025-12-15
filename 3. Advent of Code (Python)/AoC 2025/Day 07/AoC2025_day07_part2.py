#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

# create empty list of length of the number of columns to store number of lasers at each position and add initial laser
laser_set = [0 for _ in input_array[0]]
laser_set[input_array[0].index("S")] += 1

# for each row in the laser tree... 
# 1. generate list of splitters, 
# 2. check if laser exists in that position,
# 3. if yes, remove number of lasers from there and add them to idx+1, idx-1 
# don't need to worry about editing array mid loop because there are no splitters adjacent
for row in input_array:

    # locations of spliters in this row
    splitter_list = [i for (i, char) in enumerate(row) if char == "^"]

    for splitter in splitter_list:
        num_lasers =laser_set[splitter]
        if num_lasers > 0:
            laser_set[splitter]    = 0
            laser_set[splitter+1] += num_lasers
            laser_set[splitter-1] += num_lasers

    # END for splitters in row
# END for rows

# print solution
print(sum(laser_set))
