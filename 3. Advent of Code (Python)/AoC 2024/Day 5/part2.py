# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:22:34 2024

@author: crbon
"""


from copy import deepcopy

input_file = open("input","r")

input_array = input_file.read().splitlines()

# where list splits from print instructions to pages to print
split_index = input_array.index("")

# separate print ordering instructions and pages to print
print_instructions = input_array[:split_index]
print_pages = input_array[split_index+1:]

# sort to make development easier (it doesn't actually matter)
# print_instructions.sort()


## create a dictionary of lists for instructions
# each key includes pages the key must be printed before
# each key is a number and the value is a list of numbers it must come before
print_instruction_dict = {}
# for each instruction...
for instr in print_instructions:
    # get left and right side of instructions (before / after ordering) 
    left, right = instr.split("|")
    # if key already exists, append value to list, else create key in dict
    if left in print_instruction_dict:
        print_instruction_dict[left].append(right)
    else:
        print_instruction_dict[left] = [right]

## function to test if a layout is valid
def test_layout(layout_list):
    # for each element in the layout
    for i in range(len(layout_list)):
        page = layout_list[i]
        # check if it has a key in the dict (if not, it is automatically valid)
        if page in print_instruction_dict:
            dict_list = print_instruction_dict[page]
            # for each element in the dict's value, check that it doesn't come before the page
            for j in range(i):
                if layout_list[j] in dict_list:
                    # if failed, invalid return 0
                    return 0
    # test success, return middle value 
    return int(layout_list[int((len(layout_list)-1)/2)])


## Function to fix invalid layouts
# 1. pair down dictionary to only include relevant numbers in the keys/value lists
# 2. create new list and insert each element at the latest possible position it can go based on rules
# 3. return middle element of new list
## NOTE: Step 1 is actually unnecessary, commented out
def fix_layout(layout_list, print_dict):
    
    # # remove unnecessary keys from dict
    # for key in list(print_dict.keys()):
    #     if not key in layout_list:
    #         del print_dict[key]
    
    # # remove unnecessary values from dict
    # for value_list in print_dict.values():
    #     i = 0
    #     while i < len(value_list):
    #         value = value_list[i]    
    #         if not value in layout_list:
    #             value_list.remove(value)
    #         else: 
    #             i = i+1
        
    # create new list and insert pages into it
    new_list = []
    for i in range(len(layout_list)):
        value = layout_list[i]
        # if page isn't in list, the restriction list is [], else its what's in the dict
        if value in print_dict:
            value_instr = print_dict[value]
        else:
            value_instr = []

        # start by assuming the page goes at the end of the list
        max_index = len(new_list)
        # for each restriction from the dict, test to see if the page's index must be reduced
        for restriction in value_instr:
            if restriction in new_list:
                max_index = min(max_index, new_list.index(restriction))
        new_list.insert(max_index,value)
        

    return int(new_list[int((len(layout_list)-1)/2)])

middle_sum = 0
for layout_str in print_pages:
    layout_list = layout_str.split(",")
    valid_layout = test_layout(layout_list)
    
    temp_instr = deepcopy(print_instruction_dict)
    if (not valid_layout):
        middle_sum = middle_sum + fix_layout(layout_list, temp_instr)
        
        
    
print(middle_sum)
