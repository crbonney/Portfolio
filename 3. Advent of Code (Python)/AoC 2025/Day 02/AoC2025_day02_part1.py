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
    
    id_num = min_id

    while id_num <= max_id :

        # get length of ID using floor of log log (assumes id's are positive)
        id_len = math.floor(math.log10(id_num)) + 1

        # odd length, skip until reaches even numbers
        if id_len %2 == 1:
            id_num = 10**(id_len) 
            continue


        # get first half of the sequence, check if its min_id < match < max_id
        first_half = id_num // 10**(id_len//2)
        match_sequence_id = first_half + first_half*(10**(id_len//2)) 
        
        if (match_sequence_id <= max_id and match_sequence_id >= min_id):
            count_invalid += match_sequence_id

        # increase id_num first_half by 1
        id_num = (first_half+1)*(10**(id_len//2)) # handles overflow with odd-length checking

    # END while id_num <= max_id
 
        

    
# END for id_range
    
# print solution
print(count_invalid)