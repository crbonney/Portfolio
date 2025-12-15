# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 10:53:14 2024

@author: crbon
"""

### PARSE INPUT

input_file = open("input","r")

### PART 1

## Tests to determine if a report is safe
def test_safe(level_list):
    # tests if the list should be increasing or decreasing
    # multiplies results by -1 if should be decreasing
    inc_dec_multiplier = ((level_list[0] < level_list[1])-0.5)*2
    
    # confirm all entries are inc/dec and within [1,2,3] difference
    for i in range(len(level_list)-1):
        # difference between values, inverted if list should be decreasing
        diff = (level_list[i+1] - level_list[i])*inc_dec_multiplier
        
        # if outside range, return false
        if (diff < 1 or diff > 3):
            return False
        
    # passed whole list, return true
    return True

## Loop through all reports, test if they are safe
num_safe = 0
while line := input_file.readline():
    
    # split by " " and cast as int
    levels = [int(x) for x in line.split(" ")]
    safe = False
    # tests all combinations of taking out one level
    for j in range(len(levels)):
        if (test_safe(levels[0:j] + levels[j+1:len(levels)])):
            safe = True
    num_safe = num_safe + 1*safe
    
print(num_safe)

