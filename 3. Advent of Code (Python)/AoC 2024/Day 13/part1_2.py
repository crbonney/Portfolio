# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:47:04 2024

@author: crbon
"""

import re


### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

i=0
token_sum1 = 0
token_sum2 = 0
tolerance = 10**(-3)
while i < len(input_array):

    
    ## Parses the lines to get the x and y values 
    regexp = "[\+\=](\d*)"
    A_press = re.findall(regexp, input_array[i+0])
    B_press = re.findall(regexp, input_array[i+1])
    goal_res= re.findall(regexp, input_array[i+2])

    # create coefficients for system of equations to solve
    A_x = int(A_press[0])
    A_y = int(A_press[1])
    B_x = int(B_press[0])
    B_y = int(B_press[1])

    goal_x = int(goal_res[0])
    goal_y = int(goal_res[1])

    ## PART 1

    ## Cramer's Rule to solve system without introducing floating point errors
    detA = A_x*B_y - A_y*B_x;
    detA1 = goal_x*B_y - goal_y*B_x;
    detA2 = A_x*goal_y - A_y*goal_x;

    
    result = [detA1/detA, detA2/detA]

    ## checks if result is an integer without floating point errors
    if (detA1 % detA == 0 and detA2 % detA == 0): 
        token_sum1 += round(result[0]*3 + result[1])

    ## PART 2
    goal_x += 10000000000000
    goal_y += 10000000000000

    ## Cramer's Rule to solve system without introducing floating point errors
    detA = A_x*B_y - A_y*B_x;
    detA1 = goal_x*B_y - goal_y*B_x;
    detA2 = A_x*goal_y - A_y*goal_x;

    
    result = [detA1/detA, detA2/detA]

    ## checks if result is an integer without floating point errors
    if (detA1 % detA == 0 and detA2 % detA == 0): 
        token_sum2 += round(result[0]*3 + result[1])


    i+=4

print("part 1", token_sum1)
print("part 2", token_sum2)
