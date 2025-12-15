#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

# find where the blank line is
break_idx = input_array.index("")

# split input into id ranges and ingredient ids at the blank line
id_range_list = input_array[:break_idx]
ingredient_id_list = input_array[break_idx+1:]

num_fresh = 0

# for each ingredient, check valid ID ranges until valid range is found (or all ranges are checked)
for ingredient_id in ingredient_id_list:
    # print(ingredient_id)
    ingredient_id = int(ingredient_id)
    
    for id_range in id_range_list:
        id_range = id_range.split("-")
        min_id = int(id_range[0])
        max_id = int(id_range[1])
        
        # ingredient ID is within range -> it is fresh, move to next ingredient
        if ingredient_id >= min_id and ingredient_id <= max_id:
            num_fresh += 1
            # print(ingredient_id)
            break


# print solution
print(num_fresh)