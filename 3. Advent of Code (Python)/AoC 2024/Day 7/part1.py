# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:23:47 2024

@author: crbon
"""

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


result = 0
count = 0
# FOR ALL INPUTS
for x in input_array: 
    count += 1
    if (count % 50 == 0):
        print("progress: ", count, "/", len(input_array))

    # separate result and operands
    x = x.split(": ")
    x[1] = x[1].split(" ")
        
    # calculate number of combinations of +/*
    num_combinations = 2**(len(x[1])-1)

    
    # print(x)

    ## LOOP THROUGH ALL COMBINATIONS OF +/*
    for i in range(num_combinations):

        # binary decode the combination of +/*
        binary_conversion = " " #start with blank since first digit is always added to start
        for __ in range(len(x[1])-1):
            if i%2 == 0: binary_conversion += "+"
            else:        binary_conversion += "*"
            i = int(i/2)

        # alwayst start by adding first digit
        sum = int(x[1][0])
        d = 1
        ## PERFORM OPPERATIONS
        while d < len(x[1]):
            if binary_conversion[d] == "+": sum += int(x[1][d])
            else:                           sum *= int(x[1][d])    
            d+=1

        # if found a valid combination, stop checking
        if sum == int(x[0]):
            result += sum
            break
        ## END PERFORM OPERATIONS LOOP
    ## END LOOP COMBINATIONS
## END FOR ALL
print("result: ", result)
        
        