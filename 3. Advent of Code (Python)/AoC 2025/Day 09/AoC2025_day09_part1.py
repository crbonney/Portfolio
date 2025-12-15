#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

coordinate_list = [[int(i) for i in coord.split(",")] for coord in input_array]
num_points = len(coordinate_list)

# for each pair of points, compute the size of the rectangle. store the largest
# start j at i+1 to skip duplicates
max_rectangle = 0
for i in range(num_points):
    for j in range(i+1, num_points):
        
        point_1 = coordinate_list[i]
        point_2 = coordinate_list[j]

        # N-dimension length = 1+(difference in N-coordinates)
        rect_area = (1+abs(point_1[0]-point_2[0]))*(1+abs(point_1[1]-point_2[1]))

        if rect_area > max_rectangle:
            max_rectangle = rect_area
        


# # print solution
print(max_rectangle)