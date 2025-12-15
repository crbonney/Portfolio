#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()



# get list of operators, removing extra white spaces
operator_list = [i for i in input_array[-1].split(" ") if i]
elements_list = [[int(num) for num in row.split(" ") if num] for row in input_array[:-1]]


num_rows = len(elements_list)  
num_cols = len(operator_list)


# outer loop over columns to traverse vertically for each operation
sum_operations = 0
for c in range(num_cols):
    operation_elements = []
    for r in range(num_rows):
        operation_elements.append(elements_list[r][c])
        
    if operator_list[c] == "*":
        sum_operations += math.prod(operation_elements)
    elif operator_list[c] == "+":
        sum_operations += sum(operation_elements)
    else: print("ERROR")

    # END for rows
# END for columns

# print solution
print(sum_operations)
        