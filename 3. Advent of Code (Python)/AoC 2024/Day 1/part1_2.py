# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import collections

### PARSE INPUT
input_file = open("input","r")

list1 = []
list2 = []

## parse each line
# := defines the variable while checking if it is valid for while loop
while line := input_file.readline():

    # split line into parts
    parts = line.split("   ")
    # append each part into its respective column
    list1.append(int(parts[0]))
    list2.append(int(parts[1][0:5])) #[0:5] removes \n at end of line
    
    
### PART 1
## SORT LISTS
list1.sort()
list2.sort()

## SUM THEIR DIFFERENCES
sum = 0
for i in range(len(list1)):
    sum = sum + abs(list1[i] - list2[i])
    
## PRINT RESULT
print(sum)


### PART 2
## count instances of each number in each list
list1_counter = collections.Counter(list1)
list2_counter = collections.Counter(list2)

## for each number in list1_counter, multiply it by its count times its count in list2_counter
sum = 0
for num,count in list1_counter.items():    
    sum = sum + num*count*list2_counter[num]
        
print(sum)


