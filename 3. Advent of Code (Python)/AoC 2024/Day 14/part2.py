# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:49:44 2024

@author: crbon
"""

import re
import cv2
import numpy as np

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()


# width = 11
# height = 7

width = 101
height = 103

# seconds = 100


def get_pos_img(pos_list,num):
    
    pos_img = np.zeros([height,width])

    for bot in pos_list:
        pos_img[bot[0]][bot[1]] = 255
    # for r in range(height):
    #     row_str = []
    #     for c in range(width):
    #         num_bots = pos_list.count([r,c])
    #         if num_bots == 0: row_str.append(0)
    #         else: row_str.append(num_bots)
    #     pos_img.append(row_str)
    # pos_img = np.array(pos_img)
    # max_count = np.max(pos_img)
    
    # pos_img *= int(255/max_count)
    cv2.imwrite("sec" + str(num+1) + ".png", pos_img)
    
    # return pos_img      

pos_list = []
vel_list = []
i = 0
while i < len(input_array):

    ## Parses the lines to get the x and y values 
    regexp = "[\+\=](-?\d*),(-?\d*)"
    robot = re.findall(regexp, input_array[i+0])
    # robot = re.findall(regexp, "p=2,4 v=2,-3")

    # note x,y are backwards to row/col so we switch them here
    robot_pos = [int(robot[0][1]),int(robot[0][0])]
    robot_vel = [int(robot[1][1]),int(robot[1][0])]
    
    pos_list.append(robot_pos)
    vel_list.append(robot_vel)
    
    i+=1


min_safety = float('inf')
max_safety = 0
for seconds in range(10000):

    for i in range(len(pos_list)):
    
        robot_pos = pos_list[i]
        robot_vel = vel_list[i]
    
        new_pos = [(robot_pos[0] + robot_vel[0]*1) % height, 
                   (robot_pos[1] + robot_vel[1]*1) % width]
    
        pos_list[i] = new_pos
            
    
    
    ## ALSO WORKS FOR P2: LOOKS FOR STREAKS OF CONSECUTIVE HORIZONTAL BOTS
    # check_list = pos_list.copy()
    # check_list.sort()

    # prev_bot = [-2,-2]
    # consecutive_horizontal = 0
    # for i in range(len(check_list)):
    #     curr_bot = check_list[i]
    #     # print(prev_bot, curr_bot)
    #     if curr_bot == prev_bot:
    #         continue
        
    #     if prev_bot[0] == curr_bot[0] and curr_bot[1] == prev_bot[1]+1:
    #         consecutive_horizontal += 1
    #     else:
    #         consecutive_horizontal = 0
        
    #     prev_bot = curr_bot

        # if consecutive_horizontal >= 7:
        #     get_pos_img(pos_list,__)
        #     print("consecutive streak at ", __)
        #     break
        
    
    
    q1 = [x for x in pos_list if (x[0] < int(height/2)) and (x[1] < int(width/2))] # top left
    q2 = [x for x in pos_list if (x[0] > int(height/2)) and (x[1] < int(width/2))] # bot left
    q3 = [x for x in pos_list if (x[0] < int(height/2)) and (x[1] > int(width/2))] # top right
    q4 = [x for x in pos_list if (x[0] > int(height/2)) and (x[1] > int(width/2))] # bot right
    safety_factor = len(q1)*len(q2)*len(q3)*len(q4)


    # check for outliers in the safety factor
    if safety_factor > max_safety:
        get_pos_img(pos_list,seconds)
        max_safety = safety_factor
        print("new max at", seconds)

    if safety_factor < min_safety:
        get_pos_img(pos_list,seconds)
        min_safety = safety_factor
        print("new min at", seconds)



    if seconds == 99: print("part 1 safety_factor = ", safety_factor)






