#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().split(',')

count_invalid = 0

# for each id range
for id_range in input_array:
    
    id_range = id_range.split("-")
    min_id = int(id_range[0])
    max_id = int(id_range[1])
    # print(min_id,max_id)
    

    # for each id in range, check if it is invalid and add to count            
    for id_num in range(min_id, max_id+1):
        # get length of ID using floor of log log (assumes id's are positive)
        id_len = math.floor(math.log10(id_num)) + 1
        # print(id_len)
        
        # odd length, ignore
        if id_len %2 == 1:
            continue
        
        # get first half of sequence, and check if it matches second half
        second_half = id_num % 10**(id_len//2)
        first_half = id_num // 10**(id_len//2)
        # print(first_half, second_half)
        
        if (first_half == second_half):
            print(min_id, id_num, max_id)
            count_invalid += id_num
            

    
# END for id_range
    
# print solution
print(count_invalid)