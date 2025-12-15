#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

# find where the blank line is
break_idx = input_array.index("")

# split input into id ranges and ingredient ids at the blank line
# process them into [int(min),int(max)] and int(id)
id_range_list = [[int(i) for i in id_range.split("-") ] for id_range in input_array[:break_idx]]
ingredient_id_list = [int(ingr_id) for ingr_id in  input_array[break_idx+1:]]

# presort list by min_id, then max_id (priority 10**10 on min_id is sufficient for given ID ranges)
id_range_list.sort(key= lambda x: x[0]*10**10 + x[1])
ingredient_id_list.sort()

# pre-add first range to list so loop always has a range to compare against
processed_id_range_list = [id_range_list[0]]

# for each id_range in list, check if it overlaps an existing range,
# if yes, update the existing range, if no, append it to processed list
for id_range in id_range_list:

    # only have to check overlap with last processed range because of sorting
    last_processed_range = processed_id_range_list[-1]
        
    # if start and end are both within existing range, it is redundant, skip it
    if id_range[0] >= last_processed_range[0] and id_range[1] <= last_processed_range[1]:
        continue

    # if id_range starts within the processed range AND ends after it...
    # update the ends of the processed range end
    elif id_range[0] >= last_processed_range[0] and id_range[0] <= last_processed_range[1]+1 and id_range[1] >= last_processed_range[1]:
        last_processed_range[1] = id_range[1]
    
    # if id_range ends within the processed range AND starts before it...
    # update the start of the processed range start
    elif id_range[1] >= last_processed_range[0]-1 and id_range[1] <= last_processed_range[1] and id_range[0] <= last_processed_range[0]:
        last_processed_range[0] = id_range[0]

    # doesn't overlap existing range, start a new range
    else:
        processed_id_range_list.append(id_range)

# END for id_range in id_range_list



# use pre-sorted ingredient id list and processed id range list to concurrently loop through finding valid ingredients
num_fresh = 0
ingredient_idx = 0
id_range_idx = 0
while ingredient_idx < len(ingredient_id_list) and id_range_idx < len(processed_id_range_list):
    
    # if valid ingredient, count it and move to next ingredient
    if (ingredient_id_list[ingredient_idx] >= processed_id_range_list[id_range_idx][0] and
        ingredient_id_list[ingredient_idx] <= processed_id_range_list[id_range_idx][1]):
        num_fresh += 1
        ingredient_idx += 1
        continue
    
    # if ingredient id is larger than current range's max id, move to next id range
    if (ingredient_id_list[ingredient_idx] > processed_id_range_list[id_range_idx][1]):
        id_range_idx += 1
        continue

    # if ingredient is less than current ranges min id, it is invalid, move to next ingredient
    if (ingredient_id_list[ingredient_idx] < processed_id_range_list[id_range_idx][0]):
        ingredient_idx += 1
        continue

# END while id indexs are within range 


# print solution
print(num_fresh)