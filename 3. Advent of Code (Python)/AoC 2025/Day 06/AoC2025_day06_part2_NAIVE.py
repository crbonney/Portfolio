#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

operator_string = input_array[-1]
# length of input strings
str_len = len(operator_string)

# max length of vertical numbers
max_el_digits = len(input_array)-1 # -1 to remove operator_string


sum_operations = 0

# pre-initiate variables of loop that will be used before being updated in loop
operation_elements = []
prev_operator = "+"

# for length of input strings, look for operator character, then perform operation until reach next operation character
for char_idx in range(str_len):

    # character is new operator...
    # process the now complete operation, and start a new one
    if operator_string[char_idx] != " ":

        # process previous operation
        if prev_operator == "*":
            sum_operations += math.prod(operation_elements)
        elif prev_operator == "+":
            sum_operations += sum(operation_elements)
        else: print("ERROR")

        # start new operation
        prev_operator = operator_string[char_idx]
        operation_elements = []

    # for each digit in column of string, add it to the element if it exists
    digits = []
    for digit in range(max_el_digits):
        # if there is a number in input_array[row][col]
        if input_array[digit][char_idx] != ' ':
            digits.append(int(input_array[digit][char_idx]))
    # END for digits in column
    
    # process digits into an element (if there are any)
    if (len(digits) != 0):
        element = sum([digits[i]*10**(len(digits)-i-1) for i in range(len(digits))])
        operation_elements.append(element)
       

# process last operation    
if prev_operator == "*":
    sum_operations += math.prod(operation_elements)
elif prev_operator == "+":
    sum_operations += sum(operation_elements)
else: print("ERROR")

# start new operation
prev_operator = operator_string[char_idx]
operation_elements = []


# print solution
print(sum_operations)
        