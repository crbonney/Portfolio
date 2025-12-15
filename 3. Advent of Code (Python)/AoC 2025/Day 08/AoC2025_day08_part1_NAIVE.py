#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import math

### PARSE INPUT
input_file = open("input1", "r")
input_array = input_file.read().splitlines()

# process the box positions into [X,Y,Z] coordinates
box_pos_list = [[int(i) for i in box_pos.split(",")] for box_pos in input_array]

num_boxes = len(box_pos_list)

# create empty list of sets to store connected boxes
circuit_set_list = []


# calculate the distance between every pair of boxes, and store result in list
box_dist_list = []
for i in range(num_boxes):
    box_1 = box_pos_list[i]

    # start second box at i+1 to skip duplicates and same-box comparison
    for j in range(i+1, num_boxes):

        box_2 = box_pos_list[j]

        pair_dist = ((box_1[0]-box_2[0])**2 + 
                     (box_1[1]-box_2[1])**2 + 
                     (box_1[2]-box_2[2])**2)

        box_dist_list.append((i,j,pair_dist))


# sort box_dist_list by distances
box_dist_list.sort(key= lambda box_pair: box_pair[2])


# while cables are still available
# traverse sorted box pair list, applying cables if box pairs aren't in the same circuit, skipping if they are
num_cables = 10
box_dist_list_idx = 0
circuit_set_list = [] # uses lists of sets to make duplicate checking easier
connections = 0
while (num_cables > 0):

    box_1_idx = box_dist_list[box_dist_list_idx][0]
    box_2_idx = box_dist_list[box_dist_list_idx][1]

    box_dist_list_idx += 1
    
    # look for a both boxes in a circuit
    box_1_circuit = None
    box_2_circuit = None
    for circuit in circuit_set_list:

        # if boxes are in the same circuit, no need for a new connection
        if box_1_idx in circuit:
            box_1_circuit = circuit

        if box_2_idx in circuit:
            box_2_circuit = circuit



    # circuit found for both boxes, combine their circuits
    if box_1_circuit == box_2_circuit and box_1_circuit != None:
        # print(box_1_idx, box_2_idx, circuit_set_list)
        pass
    elif box_1_circuit != None and box_2_circuit != None:
        circuit_union = box_1_circuit.union(box_2_circuit)
        circuit_set_list.remove(box_1_circuit)
        circuit_set_list.remove(box_2_circuit)
        circuit_set_list.append(circuit_union)
    elif box_1_circuit != None:
        box_1_circuit.add(box_2_idx)
    elif box_2_circuit != None:
        box_2_circuit.add(box_1_idx)
    else:
        circuit_set_list.append(set([box_1_idx,box_2_idx]))

                    
    print(box_pos_list[box_1_idx], "-", box_pos_list[box_2_idx])
    num_cables -= 1
    # print(num_cables)
    

# END while cables remain


# sort circuit_sets by length
circuit_set_list.sort(reverse=True, key= lambda x: len(x))
# print solution
print(len(circuit_set_list[0])*len(circuit_set_list[1])*len(circuit_set_list[2]))