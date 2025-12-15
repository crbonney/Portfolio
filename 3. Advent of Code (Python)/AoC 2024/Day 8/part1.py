# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 00:16:09 2024

@author: crbon
"""

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

rows = len(input_array)
cols = len(input_array[0])

antenna_dict = {}

# make a dictionary with all antennas and their locations
## FOR ALL SQUARES IN INPUT
for i in range(rows):
    for j in range(cols):
        # ignore "."
        if input_array[i][j] == ".":
            continue
        char = input_array[i][j]
        if char in antenna_dict:
            antenna_dict[char].append([i,j])
        else:
            antenna_dict[char] = [[i,j]]
## END FOR ALL SQUARES            


antinode_list = []
## FOR ALL TYPES OF ANTENNAS
for char in antenna_dict:
    
    antenna_list = antenna_dict[char]
    # print(char)
    # print(antenna_list)
    ## DOUBLE LOOP THROUGH ALL COMBINATIONS OF ANTENNA
    for i in range(len(antenna_list)):
        for j in range(len(antenna_list)):
            # antenna cant match with itself
            if i == j: continue
        
            # print("antennas:", antenna_list[i], antenna_list[j])
                    
            row_diff = antenna_list[i][0] - antenna_list[j][0]
            col_diff = antenna_list[i][1] - antenna_list[j][1]
            
            # print("row/col diffs: ", row_diff, col_diff)

            

            antinode1 = [antenna_list[i][0]+row_diff,
                         antenna_list[i][1]+col_diff]
            antinode2 = [antenna_list[j][0]-row_diff,
                         antenna_list[j][1]-col_diff]
            
            # print(antinode1,antinode2)
            
            # possible antinodes are location [i] - diffs OR [j] + diffs
            # valid if they are within bounds of map
            if  0 <= antinode1[0] < rows and 0 <= antinode1[1] < cols and antinode1 not in antinode_list:
                    antinode_list.append(antinode1)
                    # print('adding a1')
            if  0 <= antinode2[0] < rows and 0 <= antinode2[1] < cols and antinode2 not in antinode_list:
                    antinode_list.append(antinode2)
                    # print('adding a2')

## END FOR ALL ANTENNA TYPES

print("result: ", len(antinode_list))
