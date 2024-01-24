import sys
from collections import defaultdict 
import networkx as nx

lines = open(sys.argv[1]).read().split('\n')

G = nx.Graph()

NODES = defaultdict(set)
for l in lines:
    node, neighbors = l.split(': ')
    neighbors = neighbors.split()
    
    NODES[node] = NODES[node] | set(neighbors)
    for n in neighbors:
        G.add_edge(node, n, weight=1)
        NODES[n] = NODES[n] | set([node])
        
cut_value, partition = nx.stoer_wagner(G)
print(len(partition[0])*len(partition[1]))

        
        
