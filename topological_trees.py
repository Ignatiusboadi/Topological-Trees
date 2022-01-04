from collections import Counter
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

### The Fibonacci tree of height $h$ has $f_{h-1}$ and $f_{h-2}$ as its branches. 
### The code below generates the edges of $f_h$ for $h\geq1$. The f_0 is the one-vertex tree and has no edge.

def f_h_edges(h):
    '''Returns the Fibonacci tree with height h. Here, we have h edges from the root to the lowest node.'''
    initial = [h + 1]                    # initial list containing h, thus the index of the hth fibonacci number
    ini_nodes = ['0' + str(h + 1) + '0'] # this list has the h with some other strings as a node.
    root = ini_nodes[0]
    edges = []                           # a list to contain the edges to be created
    j = 1                                # keeping count of the levels
    while max(initial) > 1:              # checking the maximum element of the list initial
        final = []                       # this list keeps h-1 and h-2
        fin_nodes = []                   # this list keeps the nodes created in this iteration
        k = 0                            # initial value of the indices of nodes to be added.
        for i in initial:                # iterating over elements contained in the list, initial
            if i > 1:                    # if the i which is in initial is greater than 1
                final.extend([i - 1, i - 2])                      # append i-1 and i-2
                fin_nodes.append(str(j) + str(i - 1) + str(k))    # creating the nodes and appending to fin_nodes
                fin_nodes.append(str(j) + str(i - 2) + str(k))
                edges.append((ini_nodes[k], fin_nodes[-1]))       # creating an edge between i and i-1 and i-2
                edges.append((ini_nodes[k], fin_nodes[-2]))
            k += 1                   # keeping track of the indices and number of iterations
        initial = final              # assigning final to initial and starting from the top of the iteration
        ini_nodes = fin_nodes        # assigning fin_nodes to ini_nodes
        j += 1                       # increasing the count for the levels
    return edges                     # returning the edges created.

### The code below adds the edges created from the above code to a graph.

def f_h_graph(h):
    F = nx.Graph()
    F.add_edges_from(f_h_edges(h))
    return F

### The code below creates the edges of the complete $d$-ary tree, $C_h^d$, 
### where $h$ = height and $d$ = outdegree of each internal vertex

def c_d_h(d, h):
    ini_v = ['0' + str(h)]                      # creating the root
    fin_edges = []                              # where all the edges created will be stored
    for i in range(1, h + 1):                   # counting down the height of the tree from level 1 to level h
        new_vs = list(range(d**i))                     # creating all vertices at level i.
        new_v = []                                     # temporary storage of all vertices at level i.
        for n,j in enumerate(ini_v):                   # iterating over vertices at level i-1.
            for k in new_vs[n*d:(n + 1)*d]:            # iterating over the nth d vertices at level i.
                new_v.append(str(i) + str(k))          # naming vertices at level i.
                fin_edges.append((j, str(i) + str(k))) # creating edges between the nth vertex at level i-1 and 
                                                       # nth d vertices at level i.
        ini_v = new_v           # vertices at level i now becomes the vertices at level i-1 and we proceed to the next level.
    return fin_edges    

def c_d_h_graph(d, h):
    F = nx.Graph()
    F.add_edges_from(c_d_h(d, h))
    return F

### The code below creates the edges of the $d$-ary caterpillar, $F_n^d$, 
### where $n$ = number of leaves and $d = $ outdegree of each internal vertex on the backbone of the caterpillar.

def f_d_n(d, n):
    h = (n - 1)//(d - 1)                  # calculating the height
    edges = []                            # where the edges are going to be stored
    bone = nx.path_graph(h)               # creating the backbone of the caterpillar
    edges.extend(list(bone.edges()))      # adding the edges on the backbone to the list of edges
    
    # attaching d-1 leaves to each internal vertex except the one at the highest level
    for i in list(bone.nodes())[:-1]: 
        for j in range(d-1):
            edges.append((i, str(i) + str(j)))
            
    # attaching d leaves to the internal vertex at the highest level
    vertex = list(bone.nodes())[-1]
    for k in range(d):
        edges.append((vertex, str(k) + str(vertex)))
        
    return edges

def f_d_n_graph(d,n):
    F = nx.Graph()
    F.add_edges_from(f_d_n(d, n))
    return F

### Counting the number of leaves of a given graph

def leaves(g, leaf=None):                         # input the graph and an option to print leaves or not
    degrees = dict(g.degree())                    # computing the degrees of vertices in the graph
    degree_counts = Counter(degrees.values())     # counting the number of vertices with a particular degree
    if leaf != None:                                    # if we want to print the leaves
        leafs = [i for i in degrees if degrees[i] == 1] # this adds vertices with degree 1
    else: leafs = []                                    # if we don't want to print leaves, assign leaf to []
    return degree_counts[1], leafs                # return number of vertices with degree 1 and leaves.
