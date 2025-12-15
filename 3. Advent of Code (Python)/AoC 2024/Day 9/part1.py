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
for i in range(len(input_array)):
    # even "i" are disk space - floor(i/2) to only increase the ID for every disk space
    if i%2 == 0: char = str(int(i/2))
    # odd "i" are empty space and don't increase ID count
    else:        char = "."

    # append disk to array requisite times
    for __ in range(int(input_array[i])):
        disk_map.append(char)
    
  
i = 0
j = len(disk_map)-1
## WHILE SORTING DISK MAP
# search array from both ends and end when they meet in the middle
while i < j:
    
    # if element at "i" is already a digit, move on
    if disk_map[i] != ".":
        i += 1
        continue

    # if element at "j" is not a digit, continue looking down until you find a digit    
    if disk_map[j] == ".":
        j -= 1
        continue

    ## if we reach here, disk_map[i] is a "." and disk_map[j] is a digit    
    # swap elements i and j
    disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
    
## END WHILE SORTING


i = 0
checksum = 0
## CREATE CHECKSUM
while (char := disk_map[i]) != ".":
    
    checksum += int(char)*i
    
    i += 1
    
## END WHILE CHECKSUM

print("checksum: ", checksum)