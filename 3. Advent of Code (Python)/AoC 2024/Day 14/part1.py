# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:49:44 2024

@author: crbon
"""

import re

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


width = 101
height = 103
seconds = 100


final_pos_list = []
i=0
while i < len(input_array):

    
    ## Parses the lines to get the x and y values 
    regexp = "[\+\=](-?\d*),(-?\d*)"
    robot = re.findall(regexp, input_array[i+0])
    # robot = re.findall(regexp, "p=2,4 v=2,-3")

    # note x,y are backwards to row/col so we switch them here
    robot_pos = [int(robot[0][1]),int(robot[0][0])]
    robot_vel = [int(robot[1][1]),int(robot[1][0])]

    new_pos = [(robot_pos[0] + robot_vel[0]*seconds) % height, 
               (robot_pos[1] + robot_vel[1]*seconds) % width]

    final_pos_list.append(new_pos)
    
    i += 1
    
q1 = [x for x in final_pos_list if (x[0] < int(height/2)) and (x[1] < int(width/2))] # top left
q2 = [x for x in final_pos_list if (x[0] > int(height/2)) and (x[1] < int(width/2))] # bot left
q3 = [x for x in final_pos_list if (x[0] < int(height/2)) and (x[1] > int(width/2))] # top right
q4 = [x for x in final_pos_list if (x[0] > int(height/2)) and (x[1] > int(width/2))] # bot right

safety_factor = len(q1)*len(q2)*len(q3)*len(q4)
print("safety_factor = ", safety_factor)

