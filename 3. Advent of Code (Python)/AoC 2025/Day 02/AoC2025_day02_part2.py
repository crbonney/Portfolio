#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().split(',')

count_invalid = 0

# list of divisors for to get 2+ copies of a sequence for each ID length
# table index represents number of digits in ID
divisor_table = [[],        #0
                 [],        #1 - length 1 can't have any sequences that repeat twice
                 [1],       #2
                 [1],       #3
                 [1,2],     #4
                 [1],       #5
                 [1,2,3],   #6
                 [1],       #7
                 [1,2,4],   #8
                 [1,3],     #9
                 [1,2,5],   #10
                 [1],       #11
                 [1,2,3,4,6],#12
                 [1]        #13
]

# for each id range
for id_range in input_array:
    
    id_range = id_range.split("-")
    min_id = int(id_range[0])
    max_id = int(id_range[1])
    # print(min_id,max_id)
    
    id_num = min_id

    # use id lengths to limit possible sequence lengths
    min_id_length = math.floor(math.log10(min_id)) + 1
    max_id_length = math.floor(math.log10(max_id)) + 1

    id_length_range = range(min_id_length,max_id_length+1)

    invalid_id_list = set() # use set to automatically handle duplicates (1111 is invalid as 4 1's and 2 11's)
        

    while id_num <= max_id :

        # get length of ID using floor of log log (assumes id's are positive)
        id_len = math.floor(math.log10(id_num)) + 1

        # get possible sequence lengths for current id_length
        divisors = divisor_table[id_len] 



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