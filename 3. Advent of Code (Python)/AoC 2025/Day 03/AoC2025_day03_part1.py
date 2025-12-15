#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

sum_joltage = 0

# for each joltage bank, find the largest value EXCEPT the last cell
# then find the second largest cell after that (including last cell)
for bank in input_array:
    
    max_jolt = 0
    second_max_jolt = 0
    
    # for each cell in bank
    for i in range(len(bank)-1):
        
        cell_joltage = int(bank[i])
        
        # check if cell is the new largest, or the new largest successor
        if cell_joltage > max_jolt:
            max_jolt = cell_joltage
            second_max_jolt = 0
        elif cell_joltage > second_max_jolt:
            second_max_jolt = cell_joltage 
    # END for each cell
            
    # check if the last cell is the largest that follows the max
    cell_joltage = int(bank[-1])
    if cell_joltage > second_max_jolt:
        second_max_jolt = cell_joltage
    
    sum_joltage += max_jolt*10 + second_max_jolt
# END for bank in input_array

    
# print solution
print(sum_joltage)