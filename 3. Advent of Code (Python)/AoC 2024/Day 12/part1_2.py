# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:39:34 2024

@author: crbon
"""

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

def is_diagonal(square1, square2):

    # are they same row and cols differ by 1?  
    if abs(square1[0]-square2[0]) == 1 and abs(square1[1]-square2[1]) == 1:
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

## loop through all the plots and add up their prices
total_price = 0
total_price_w_discount = 0
for plot_key in plots:
    
    cur_plot = plots[plot_key]
    
    perimeter = cur_plot[0][0]
    # remove perimeter tracker entry after we use it
    del cur_plot[0]
    
    # number of squares in plot
    area = len(plots[plot_key]) 



    # calculate the number of sides in the plot
    num_sides = 0

    ## SCAN EACH PLOT TWICE (range(2))
    ## first loop is vertical scan (top/bottom sides), 
    ## then transpose rows and cols at end of first loop and scan again (left/right sides)
    for __ in range(2):
        cur_plot.sort()
        # print(cur_plot)

        i = 0
        # init sides to impossible indices for first comparison
        last_top_side = [-2,-2]
        last_bot_side = [-2,-2]
        
        ## FOR ALL SQUARES IN PLOT
        while i < area: 
            
            square = cur_plot[i]    
            # print(square)
    
            ## for each square...            
            ## TOP
            # check if square has a neighbor above (is a top)
            # AND previous edge wasn't left neighbor so we don't double count
            ## BOTTOM
            # check if square has a neighbor below (is a bottom)
            # AND previous edge wasn't left neighbor so we don't double count
            
    
            # TOP: if no neighbors above...
            if [square[0]-1,square[1]] not in cur_plot:
                # AND left neighbor wasn't counted as a side (or is in a different row)
                # print(last_top_side, cur_plot[i-1])
                if last_top_side != [square[0],square[1]-1]:
                    num_sides += 1
                    # print(square, "new top, total: ", num_sides)
                last_top_side = square
    
            
            # BOT: if no neighbors below...
            if [square[0]+1,square[1]] not in cur_plot:
                # AND left neighbor wasn't counted as a side
                if last_bot_side != [square[0],square[1]-1]:
                    num_sides += 1            
                    # print(square, "new bot, total: ", num_sides)
                last_bot_side = square
            
            i += 1
        ## VERTICAL SCAN WHILE LOOP END
    
        # transpose rows/cols
        cur_plot = [[x[1],x[0]] for x in cur_plot]
    ## SIDE COUNTING LOOP END
    
    
    # print(plot_key, ":")
    # print(num_sides,"sides")    

    ## PART 1
    price = area*perimeter
    price_w_discount = area*num_sides

    total_price += price
    total_price_w_discount += price_w_discount

print("total price",total_price)
print("total price with discount",total_price_w_discount)