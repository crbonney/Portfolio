# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:22:34 2024

@author: crbon
"""

input_file = open("input","r")

input_array = input_file.read().splitlines()

# where list splits from print instructions to pages to print
split_index = input_array.index("")

print_instructions = input_array[:split_index]
print_pages = input_array[split_index+1:]

print_instructions.sort()


## create a dictionary of lists for instructions
# each key includes pages the key must be printed before
print_instruction_dict = {}
for instr in print_instructions:
    left, right = instr.split("|")
    # left = int(left)
    # right = int(right)
    if left in print_instruction_dict:
        print_instruction_dict[left].append(right)
    else:
        print_instruction_dict[left] = [right]

def test_layout(layout_list):
    for i in range(len(layout_list)):
        page = layout_list[i]
        dict_list = print_instruction_dict[page]
        for j in range(i):
            if layout_list[j] in dict_list:
                return 0
    return int(layout_list[int((len(layout_list)-1)/2)])

middle_sum = 0
for layout_str in print_pages:
    layout_list = layout_str.split(",")
    middle_sum = middle_sum + test_layout(layout_list)
    
print(middle_sum)
