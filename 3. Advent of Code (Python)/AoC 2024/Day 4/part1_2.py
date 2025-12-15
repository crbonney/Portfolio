# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 12:33:32 2024

@author: crbon
"""

### PARSE INPUT
input_file = open("input","r")
input_array = input_file.read().splitlines()


width = len(input_array[0])
height = len(input_array)

total = 0
for i in range(height):
    for j in range(width):
        print(i,j)
        if (i < height-3):
            if input_array[i][j] == "X" and input_array[i+1][j] == "M" and input_array[i+2][j] == "A" and input_array[i+3][j] == "S":
                total = total+1
            if input_array[i][j] == "S" and input_array[i+1][j] == "A" and input_array[i+2][j] == "M" and input_array[i+3][j] == "X":
                total = total+1

        if (j < width-3):
            if input_array[i][j] == "X" and input_array[i][j+1] == "M" and input_array[i][j+2] == "A" and input_array[i][j+3] == "S":
                total = total+1
            if input_array[i][j] == "S" and input_array[i][j+1] == "A" and input_array[i][j+2] == "M" and input_array[i][j+3] == "X":
                total = total+1

        if (i < height-3 and j < width-3):
            if input_array[i][j] == "X" and input_array[i+1][j+1] == "M" and input_array[i+2][j+2] == "A" and input_array[i+3][j+3] == "S":
                total = total+1
            if input_array[i][j] == "S" and input_array[i+1][j+1] == "A" and input_array[i+2][j+2] == "M" and input_array[i+3][j+3] == "X":
                total = total+1
            
        if (i > 2 and j < width-3):
            if input_array[i][j] == "X" and input_array[i-1][j+1] == "M" and input_array[i-2][j+2] == "A" and input_array[i-3][j+3] == "S":
                total = total+1
            if input_array[i][j] == "S" and input_array[i-1][j+1] == "A" and input_array[i-2][j+2] == "M" and input_array[i-3][j+3] == "X":
                total = total+1
            
            
print(total)        


total = 0
for i in range(1,height-1):
    for j in range(1,width-1):
        
        x = False
        if input_array[i][j] == "A":
            if input_array[i-1][j-1] == "M" and input_array[i+1][j+1] == "S" or input_array[i-1][j-1] == "S" and input_array[i+1][j+1] == "M":
                x = True
            if input_array[i+1][j-1] == "M" and input_array[i-1][j+1] == "S" or input_array[i+1][j-1] == "S" and input_array[i-1][j+1] == "M":
                total = total+1*x

print(total)


