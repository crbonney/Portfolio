# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 12:04:50 2024

@author: crbon
"""

import re

### PARSE INPUT
input_file = open("input","r")
input_text = input_file.read()
# input_text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

## regex to find mult instructions
mul_regex = "mul\((\d{1,3}),(\d{1,3})\)"


### PART 1

## Find all mul instructions
matches = re.findall(mul_regex,input_text)

## Mult and Add them up
mult_sum = 0
for i in range(len(matches)):
    mult_sum = mult_sum + int(matches[i][0])*int(matches[i][1])
    
print(mult_sum)


### PART 2

## split input text by "do()" and "don't()"
do_dont_regex = "(do\(\)|don\'t\(\))"
split_text = re.split(do_dont_regex,input_text)


mult_sum = 0
active = True
for part in split_text:
    if part == "do()":
        active = True
    elif part == "don't()":
        active = False
    elif active:
        matches = re.findall(mul_regex,part)
        for i in range(len(matches)):
            mult_sum = mult_sum + int(matches[i][0])*int(matches[i][1])
            
print(mult_sum)
    
    
    
    
    