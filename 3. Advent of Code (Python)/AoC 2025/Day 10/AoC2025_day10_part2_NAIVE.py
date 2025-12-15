#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math
import re
import numpy as np
import sympy as sym

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

def goal_func(solution_vector):
    
    penalty = 0
    
    for i in solution_vector:
        if i < 0: penalty += abs(100*i) # harsh penalty on negative values (solution must be positive)
        else: penalty += i # small penalty on positive button presses
        
    return penalty

### PARSE INPUT
input_file = open("input", "r")
# input_array = input_file.read().splitlines()
input_string = input_file.read()

input_spliter_regex = "\[(.*?)\] (\(.*\)) \{(.*?)\}"

# regex to split input into sections "[group1] (group2) {group3}"
split_lines = re.findall(input_spliter_regex, input_string)


# for each lighting diagrom
total_button_pressed = 0
sum_buttons = 0
diagram_num = 0
for diagram_specs in split_lines:
    diagram_num+=1
    # print(diagram_num)

    # vector of goal for end state of counters
    counters_goal_vector = np.array(diagram_specs[2].split(","),dtype="int")

    num_counters = len(counters_goal_vector)

    # list of buttons, and which lights they toggle
    button_list = re.findall("\((.*?)\)", diagram_specs[1])
    num_buttons = len(button_list)

    # empty matrix to store button presses    + 1 col for augmented row goal vector
    button_counter_matrix = np.zeros((num_counters,num_buttons),dtype="int")

    # calculate which counters each button increments, and fill in matrix 
    for i in range(num_buttons):
        
        button = button_list[i]

        # which lights the button toggles
        button_lights = button.split(",")

        for j in button_lights:
            button_counter_matrix[int(j),i] = 1
            

    A = sym.Matrix(button_counter_matrix)
    b = sym.Matrix(counters_goal_vector)
    aug_matrix = A.row_join(b)
    rref_matrix = aug_matrix.rref()
    
    free_variables = [i for i in range(num_buttons) if i not in rref_matrix[1]]

    solution_matrix = rref_matrix[0]
    #insert rows for free variables into solution matrix
    for row in free_variables:
        solution_matrix = solution_matrix.row_insert(row, sym.zeros(1,num_buttons+1))
        pass

    # for each row in augmented matrix
    changed_denom = False
    for i in range(solution_matrix.shape[0]):

        # while denominators in that row are > 1, perform multiplication row operation        
        while True:
            max_denominator = max([sym.fraction(i)[1] for i in solution_matrix[i,:]])
            # if row has fraction, row multiply to remove it
            if max_denominator == 1: break
            print(solution_matrix)
            solution_matrix[i,:] *= max_denominator
            changed_denom = True
            break

    if changed_denom: exit

    # split augmented matrix
    solution_vector = solution_matrix[:,-1]
    solution_matrix = solution_matrix[:,:-1]

    
    ## ERROR IN DENOMINATOR REMOVAL
    # new algorithm:
        # - look for denominators in each row of augmented matrix
        # - multiply row by largest denominator until all denominators gone
        
        

    # print(solution_matrix, solution_vector)
    # print("initial solution:", solution_vector, ", cost: ",goal_func(solution_vector))

    # iterate until no progress is made
    gain = -1
    while gain < 0:
        
        gain = 0
        move = None
        penalty = goal_func(solution_vector)
        # print(penalty)
        # 
        for free_var in free_variables:
            
            solution_vector += solution_matrix[:,free_var]
            solution_vector[free_var] -= 1
            
            test_gain = goal_func(solution_vector) - penalty
            if test_gain < gain:
                gain = test_gain
                move = solution_matrix[:,free_var]
                move[free_var] = -1

            solution_vector += -2*solution_matrix[:,free_var]
            solution_vector[free_var] += 2

            test_gain = goal_func(solution_vector) - penalty
            if test_gain < gain:
                gain = test_gain
                move = -solution_matrix[:,free_var]
                move[free_var] = 1

            solution_vector += solution_matrix[:,free_var]
            solution_vector[free_var] -= 1

        if  move != None:
            solution_vector += move
            # print(gain, move)

    # END while iteratively improving            
    
    # print("final solution:", solution_vector, " - cost:", goal_func(solution_vector))
    print("valid solution:", A @ solution_vector[:A.shape[1],:] == b, " - denom changed: ", changed_denom)
    if changed_denom:
        exit

    sum_buttons += sum(solution_vector)
    
    


# # print solution
print(sum_buttons)