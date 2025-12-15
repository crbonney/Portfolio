#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
sign = lambda x: math.copysign(1, x)

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

coordinate_list = [[int(i) for i in coord.split(",")] for coord in input_array]
num_points = len(coordinate_list)

# for each pair of points, compute the size of the rectangle. store the largest
# start j at i+1 to skip duplicates
max_rectangle = 0
for i in range(num_points):
    print(i)
    for j in range(i+1, num_points):
        
        point_i = coordinate_list[i]
        point_j = coordinate_list[j]


        # N-dimension length = 1+(difference in N-coordinates)
        rect_area = (1+abs(point_i[0]-point_j[0]))*(1+abs(point_i[1]-point_j[1]))


        # if not a new max, skip
        # else, continue to checking if it's valid
        if rect_area <= max_rectangle: continue        
        
        # bounds of rectangle to make spotting invalid lines easier
        rect_x_range = sorted([point_i[0], point_j[0]])
        rect_y_range = sorted([point_i[1], point_j[1]])
    
        # seach through all connecting lines, starting at (i -> i+1)
        valid_rectangle = True
        for k in range(i,num_points+i+1):

            # use modulo to handle index range
            k_idx = k % num_points
            k2_idx = (k+1) % num_points

            point_k = coordinate_list[k_idx]
            point_k2 = coordinate_list[k2_idx]

            # checks if horizontal or vertical line
            vertical_line = point_k[0] == point_k2[0] 

            # print("| ", point_k, point_k2, "vertical:", vertical_line)

            # a line makes a rectangle invalid if it travels into the bounds of the rectangle
            
            if not vertical_line:
                # crosses left  boundry AND is strictly inside y-bounds
                if (sign(point_k[0]-rect_x_range[0]-0.5) != sign(point_k2[0]-rect_x_range[0]-0.5) and
                    point_k[1] >  rect_y_range[0] and point_k[1]  < rect_y_range[1]
                    ):
                    valid_rectangle = False
                    break
                
                # crosses right boundry AND is strictly inside y-bounds
                if (sign(point_k[0]-rect_x_range[1]-0.5) != sign(point_k2[0]-rect_x_range[1]-0.5) and
                    point_k[1] >  rect_y_range[0] and point_k[1]  < rect_y_range[1]
                    ):
                    valid_rectangle = False
                    break

            if vertical_line:           
                # crosses top   boundry AND is strictly inside y-bounds
                if (sign(point_k[1]-rect_y_range[0]-0.5) != sign(point_k2[1]-rect_y_range[0]-0.5) and
                    point_k[0] >  rect_x_range[0] and point_k[0]  < rect_x_range[1]
                    ):
                    valid_rectangle = False
                    break
                
                # crosses bot   boundry AND is strictly inside y-bounds
                if (sign(point_k[1]-rect_y_range[1]-0.5) != sign(point_k2[1]-rect_y_range[1]-0.5) and
                    point_k[0] >  rect_x_range[0] and point_k[0]  < rect_x_range[1]
                    ):
                    valid_rectangle = False
                    break


        # print("| valid? :", valid_rectangle)
        if valid_rectangle:
            max_rectangle = rect_area


# # print solution
print(max_rectangle)

