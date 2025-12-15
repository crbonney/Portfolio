# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:04:38 2024

@author: crbon
"""

### PARSE INPUT
input_file = open("input", "r")
input_array = input_file.read().splitlines()

rows = len(input_array)
cols = len(input_array[0])

input_array = [list(map(int,list(input_array[x]))) for x in range(rows)]


### CREATE DIRECTED GRAPH:
## for each square, create a dictionary entry that denotes where it can move to


graph_edges = {}
for r in range(rows):
    for c in range(cols):
        value = input_array[r][c]
        id_tuple = (value,r,c)
        graph_edges[id_tuple] = []
        
        ## check if its possible to traverse LEFT/RIGHT or UP/DOWN
        # if it is possible, add move to graph_dict entry 
        if r-1 >= 0 and input_array[r-1][c] == value+1:
            graph_edges[id_tuple].append((value+1,r-1,c))
        if r+1 < rows and input_array[r+1][c] == value+1:
            graph_edges[id_tuple].append((value+1,r+1,c))
        if c-1 >= 0 and input_array[r][c-1] == value+1:
            graph_edges[id_tuple].append((value+1,r,c-1))
        if c+1 < cols and input_array[r][c+1] == value+1:
            graph_edges[id_tuple].append((value+1,r,c+1))

def traverse_graph(node_id):
    global graph_edges
    global visited_edges
    global total_score

    # print("visiting", node_id)

    # Already visted this node, return
    if node_id in visited_edges: return # print("already visited")

    # else, note we have visited this node
    visited_edges.append(node_id)

    # if found trail head, add 1 to score and return
    if node_id[0] == 9: 
        total_score += 1
        # print("score++")
        return

    # if node has no edges, its a dead end - return
    if len(graph_edges[node_id]) == 0: return # print("no further edges")

        
    # if reaching this point, recurse for all edges of this node
    for edge in graph_edges[node_id]:
        traverse_graph(edge)
        


total_score = 0
for id_tuple,edges in graph_edges.items():
    # only need to start at trailheads
    if id_tuple[0] != 0: continue
    # print("trailhead: ", id_tuple)
    
    # recursive DFS from trailhead to find all reachable trail ends
    visited_edges = []
    traverse_graph(id_tuple)
    
    
print("total score:", total_score)