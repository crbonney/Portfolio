# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 01:01:43 2024

@author: crbon
"""

input_file = open("input", "r")
input_array = list(input_file.read())
# input_array.pop(-1) #removes endline

## CREATE ORIGINAL DISK MAP
disk_map = []
filled_dict = {}
empty_list = []
cur_idx = 0
for i in range(len(input_array)):
    section_len = int(input_array[i])

    # even "i" are disk space - floor(i/2) to only increase the ID for every disk space
    if i%2 == 0: filled_dict[int(i/2)] = [cur_idx,section_len]
    else:        empty_list.append([cur_idx,section_len])

    cur_idx += section_len


# a function to reorganize the list of empty sections in the disk map
def resort(empty_list):

    q = 0
    while q < len(empty_list):
        # if empty section length is 0, remove section
        if (empty_list[q][1] == 0):
            del empty_list[q]
            q -= 1
        q += 1

    empty_list.sort()
    
    q = 0
    while q < len(empty_list)-1:

        cur_end    = empty_list[q][0] + empty_list[q][1]
        next_start = empty_list[q+1][0]
        
        ## combine sections and delete later
        if cur_end == next_start:
            empty_list[q][1] += empty_list[q+1][1]
            del empty_list[q+1]
            q -= 1
        
        q += 1
    
    return empty_list

    
# highest possible id
max_id = int((len(input_array)-1)/2)

## FOR ALL FILLED SECTIONS (in reverse)
for i in range(max_id,-1,-1):

    # section_id    = i
    section_start = filled_dict[i][0]
    section_len   = filled_dict[i][1]
    
    # SEARCH FOR VALID EMPTY SECTION
    for j in range(len(empty_list)-1):
        empty_start = empty_list[j][0]
        empty_len   = empty_list[j][1]
        # empty_stop  = empty_start + empty_len
        
        # don't need to search sections to the right of section start
        if empty_start > section_start:
            break
        
        # enough space to swap in
        if section_len <= empty_len:
            # move filled spot to new location
            filled_dict[i] = [empty_start, section_len]
            
            # reduce empty range length by swapped section length and increaes its start pos
            empty_list[j][1] -= section_len
            empty_list[j][0] += section_len
                                    
            # create new empty range at previous location of filled section
            empty_list.append([section_start,section_len])
            
            ## reorganize and combine duplicates in empty list - apparently unnecessary
            # empty_list = resort(empty_list)
            
            # stop searching for swap
            break
    ## END SEARCH FOR VALID EMPTY SECTION
## END FOR ALL FILLED SECTIONS (in reverse)
            


i = 0
checksum = 0
## CREATE CHECKSUM
for key,value in filled_dict.items():
    
    # for each ID, add to the checksum sum([ID*start, ID*(start+1), ... , ID*(start+end-1)])
    checksum += sum([key*x for x in range(value[0],value[0]+value[1])])
    
## END WHILE CHECKSUM

print("".join(disk_map))
print("checksum: ", checksum)

