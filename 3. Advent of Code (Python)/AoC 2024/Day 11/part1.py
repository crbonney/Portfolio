# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:11:11 2024

@author: crbon
"""

input_file = open("input", "r")
stone_list = input_file.read().split(" ")

stone_count = {}
for key in stone_list:
    if key in stone_count:
        stone_count[key] += 1
    else: stone_count[key]= 1
    

# print(stone_list)

# transform_dict = {
#     '0': ['1'],
#     '1': ['2024']
# }

# stone_count = {
#     '125': 1,
#     '17': 1
# }

# print(stone_count)

num_blinks = 75
for blink in range(num_blinks):

    new_count = {}
    for key,value in stone_count.items():
        
        if int(key) == 0:            
            if '1' in new_count:
                new_count['1'] += value
            else: new_count['1'] = value

            continue
        
        num_len = len(key)
        if num_len % 2 == 0:
            front_half = key[:int(num_len/2)]
            back_half  = str(int(key[int(num_len/2):])) # cast as int first to remove leading 0s
            
            if front_half in new_count:
                new_count[front_half] += value
            else: new_count[front_half]= value

            if back_half in new_count:
                new_count[back_half] += value
            else: new_count[back_half]= value
            
            continue
        
        mult_num = str(int(key)*2024)
        if mult_num in new_count:
            new_count[mult_num] += value
        else: new_count[mult_num]= value
        
    ## END BLINK UPDATE LOOP
    stone_count = new_count
    print("blink ", blink+1)
    # print(stone_count)

total_stones = sum([val for val in stone_count.values()])
print("num_stones: ", total_stones)