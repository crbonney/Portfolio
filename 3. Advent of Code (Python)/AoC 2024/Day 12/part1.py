# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:39:34 2024

@author: crbon
"""

import numpy as np 
### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

num_rows = len(input_array)
num_cols = len(input_array[0])

# dict of plots, keys are locations of squares in that 
plots = {"*": [[0,-2]]}

# checks if two squares are adjacent
# input: two pairs of lists/tuples containing [r,c] of their square
def is_adjacent(square1, square2):

    # are they same row and cols differ by 1?  
    if square1[0] == square2[0] and abs(square1[1]-square2[1]) == 1:
        return True

    # are they same col and rows differ by 1?  
    if square1[1] == square2[1] and abs(square1[0]-square2[0]) == 1:
        return True

    # else not adjacent
    return False

# loops throw squares
for r in range(num_rows):

    for c in range(num_cols):
        found_plot = False

        # check plots dict to see if square is a part of an existing plots
        for plot_key in list(plots.keys()):
            
            
            # if plot name doesn't match, skip this plot (its a different plant)
            if not input_array[r][c] in plot_key:
                continue

            # else, check if plot with same name contains any squares adjacent to current square
            num_adjacent = 0
            for square in plots[plot_key]:

                # counts number of adjacent squares in current plot
                if is_adjacent(square, [r,c]):
                    num_adjacent += 1

            # if no adjacent squares found in plot, skip
            if num_adjacent == 0:
                continue

            # if there's adjacent squares and it isn't already part of a plot, add it to that plot
            if not found_plot:
                found_plot = plot_key
                plots[plot_key].append([r,c])
                if num_adjacent == 1:
                    plots[plot_key][0][0] += 2
                # if num_adjacent == 2: perimiter doesn't change
                elif num_adjacent == 3:
                    plots[plot_key][0][0] -= 2
            # if there's adjacent squares and it *is* already part of a plot, combine the plots
            else:
                # combine their perimiters
                plots[found_plot][0][0] += plots[plot_key][0][0]
                # remove the perimiter tracker from the second plot
                del plots[plot_key][0]
                # add squares of new plot to old plot
                plots[found_plot] += plots[plot_key]
                # delete new plot
                del plots[plot_key]
                # append new square NOPE IT WAS ALREADY ADDED EARLIER
                # plots[found_plot].append([r,c])
                
                # additional perimeter chance from the combination
                if num_adjacent == 1:
                    plots[found_plot][0][0] += -2
                else: # shouldn't be possible with how I loop through elements
                    print("AhLAARRM plot comination: num_adjacent = " + str(num_adjacent))
                    
                
                    
                break
            
                
                
        # square wasn't a part of any existing plot
        # create a new plot conataining it
        if not found_plot:
            plots[input_array[r][c]+str(r)+str(c)] = [[4,-2], [r,c]]

            continue
        
    
# delete placeholder plot
del plots["*"]        

total_price = 0
for plot_key in plots:
    
    perimeter = plots[plot_key][0][0]
    area = len(plots[plot_key])-1 # subtract one to remove the perimeter tracking entry
    price = area*perimeter
    print(price)
    total_price += price
    