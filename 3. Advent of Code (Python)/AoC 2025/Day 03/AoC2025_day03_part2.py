#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

sum_joltage = 0

# for each joltage bank, find the largest value with increased priority on earlier cells
for bank in input_array:
    

    # create an array to hold the 12 joltage cells
    joltage_array = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    # for each cell in bank
    for i in range(len(bank)):
        
        cell_joltage = int(bank[i])
        
        # for each cell in joltage_array, check if new cell is better (if possible)
        for j in range(len(joltage_array)):

            # only attempt to replace cells if there enough cells left in the bank to finish the array after it
            # (len(bank)-i) = remaining cells in bank // (len(joltage_array)-j) = cells required to finish array
            if (len(bank)-i < (len(joltage_array)-j)):
                continue

            # if new cell is better, replace it and wipe all entries in the array that follow
            if cell_joltage > joltage_array[j]:
                joltage_array[j] = cell_joltage
                
                # replace every cell after new stored cell with 0's
                joltage_array[j+1:] = [0 for _ in range(len(joltage_array)-j-1)]
                
                break # exit loop so it doesn't double assign

        # END for loop through joltage array
        
    # END for each cell

    # processes the joltage_array by concatenating integer entries
    sum_joltage += sum([joltage_array[i]*10**(len(joltage_array)-i-1) for i in range(len(joltage_array))])
# END for bank in input_array

    
# print solution
print(sum_joltage)