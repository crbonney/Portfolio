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
    
    

    # for each id in range, check all possible iterations of invalidness and add to count            
    for id_num in range(min_id, max_id+1):
        # get length of ID using floor of log log (assumes id's are positive)
        id_len = math.floor(math.log10(id_num)) + 1

        for divisor in divisor_table[id_len]:
                       
            id_str = str(id_num)
            id_sequence = id_str[0:divisor]
            # print("id,div,seq", id_str, divisor, id_sequence)
            idx = 0
            match = True
            while idx+divisor <= id_len:
                # print("id,seq,match_seq", id_str, id_sequence, id_str[idx:idx+divisor])
                if id_str[idx:idx+divisor] != id_sequence:
                    # print("no match")
                    match = False
                    break
                idx += divisor
            
            if match:
                count_invalid += id_num
                break                
        
            
    
# END for id_range
    
# print solution
print(count_invalid)