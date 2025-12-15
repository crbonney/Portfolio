#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math
import re

# gets a binary string representation of a number with left-most digit being least significant
def get_bin_str(num):

    # edge case of n = 0
    if (num == 0):
        return "0"
    
    bin_str = ""
    while num != 0:
        # if num
        if num % 2 == 1: bin_str += "1"
        else:            bin_str += "0"
        num //= 2

    return bin_str

### PARSE INPUT
input_file = open("input", "r")
# input_array = input_file.read().splitlines()
input_string = input_file.read()

input_spliter_regex = "\[(.*?)\] (\(.*\)) \{(.*?)\}"

# regex to split input into sections "[group1] (group2) {group3}"
split_lines = re.findall(input_spliter_regex, input_string)

# NON NAIVE IDEA: try using binary representation of lights/buttons    
# NON NAIVE IDEA: linear combination solution

# for each lighting diagrom
total_button_pressed = 0
for diagram_specs in split_lines:
    
    num_lights = len(diagram_specs[0])

    # binary representation of the lighting requirements
    # "#.#." = 1*1 + 0*2 + 1*4 + 0*8
    binary_lighting_number = 0
    for i in range(num_lights):
        binary_lighting_number += (diagram_specs[0][i] == "#")*2**i
    
    # list of buttons, and which lights they toggle
    button_list = re.findall("\((.*?)\)", diagram_specs[1])
    num_buttons = len(button_list)

    # binary represenation of button list (could be compressed into list comprehension)
    binary_button_list = []
    for button in button_list:
        
        # which lights the button toggles
        button_lights = button.split(",")

        # calculate the binary representation for each button
        button_binary = 0
        for light in button_lights:
            button_binary += 2**int(light)
        
        binary_button_list.append(button_binary)

    # print("goal lighting:", get_bin_str(binary_lighting_number))
    # print([get_bin_str(i) for i in binary_button_list])
   
    min_pressed_solution = 10**10 # infinity, or no solution found
    # for each combination of buttons, seach for min_pressed solution
    for i in range(2**num_buttons):
        i_bin_str = get_bin_str(i)
        # i = binary representation of which buttons are pressed
        lights = 0
        num_pressed = 0
        valid_solution = False
        for j in range(len(i_bin_str)):
            if i_bin_str[j] == "1":
                lights ^= binary_button_list[j]
                num_pressed += 1
                if lights ^ binary_lighting_number == 0:
                    valid_solution = True
                    break
                # print("j =", j, ", light_toggle =", get_bin_str(lights))
        if valid_solution and num_pressed < min_pressed_solution:
            min_pressed_solution = num_pressed
        # print("i_bin_str", i_bin_str, ", result =", get_bin_str(lights), ", buttons pressed =", num_pressed,  ", solution =", valid_solution)

    # print("Best solution:", min_pressed_solution)
    total_button_pressed += min_pressed_solution
    # use bitwise XOR to calculate toggles

# # print solution
print(total_button_pressed)