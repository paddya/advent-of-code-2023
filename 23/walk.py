import sys
from collections import deque, defaultdict
from heapq import heappush, heappop
from functools import cache

# We use recursion later, just be safe
sys.setrecursionlimit(100000)

# Parse the input into a two-dimensional array that represents the grid
grid = [[c for c in row] for row in open(sys.argv[1]).read().split('\n')]

WIDTH = len(grid[0])
HEIGHT = len(grid)

# Tip when working with grids: it's often a lot easier to store
# the grid as a dictionary that uses (row, column) as the key.
# This simplifies bound checks to "(r, c) in G".
G = dict()

for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        G[(r,c)] = cell

# Find the start and end nodes for the search
start = (-1, -1)
for c, cell in enumerate(grid[0]):
    if cell == '.':
        start = (0, c)
        break
end = (-1, -1)
for c, cell in enumerate(grid[HEIGHT-1]):
    if cell == '.':
        end = (HEIGHT-1, c)
        break


# Some general notes:

# Finding the longest path in a graph is NP-hard (https://en.wikipedia.org/wiki/Longest_path_problem)
# It is actually feasible to brute-force Part 1 because
# the slopes constrain the possible paths in a way that keeps
# the total number of paths manageable.


# Translate the slopes into a direction vector
mv = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0)
}


# Looking at the input, we can see that the grid resembles a
# labyrinth with many long paths between crossings.
# Therefore, we can transform our grid into a graph that
# only contains the crossings as nodes and weighted
# edges that link the crossings like in the original grid.

# Our first step involves finding all crossings in the graph.
# Consider the following input:

#.#####
#...###
###.###
#..x..#
#.###.#
#####.#

# A crossing is a cell that has more than two neighbors. In the example
# input, there is only one crossing and it is marked with "x".

NUM_NEIGHBORS = dict()
CROSSINGS = set()

for (r,c), cell in G.items():
    if cell == '#':
        continue
    numNeighbors = 0
    for (mr,mc) in mv.values():
        rr = r+mr
        cc = c+mc
        if (rr,cc) in G and G[(rr,cc)] != '#':
            numNeighbors += 1
    
    NUM_NEIGHBORS[(r,c)] = numNeighbors
    if numNeighbors != 2:
        CROSSINGS.add((r,c))


# findEdges() is a helper that finds the neighbors and their
# distance for a given crossing.
def findEdges(start, withSlopes = True):
    Q = deque([(start, 0)])
    visited = set({start})
    
    edges = []
    
    while len(Q) > 0:
        current, pathLen = Q.popleft()
        if current != start and current in NUM_NEIGHBORS and (current == end or NUM_NEIGHBORS[current] > 2):
            edges.append((current, pathLen))
            continue
            
        r,c = current
        movements = []
        if G[(r,c)] == '.' or not withSlopes:
            movements = mv.values()
        else:
            movements = [mv[G[(r,c)]]]
        
        for (mr, mc) in movements:
            rr = r + mr
            cc = c + mc
            
            if (rr, cc) in G and G[(rr,cc)] != '#' and (rr, cc) not in visited:
                Q.append(((rr,cc), pathLen+1))
                visited.add((rr, cc))
                
    return edges

# edgeBfs() runs a breadth-first search that finds
# all possible paths in the graph. In order to achieve this,
# we store the set of visited nodes as part of the state that
# is written to the visited set. This makes it possible to reach
# the same spot in the grid multiple times but on different paths
# (= a different set of already visited nodes).
def edgeBfs(start, end, withSlopes):
    EDGES = dict()
    for c in CROSSINGS:
        EDGES[c] = findEdges(c, withSlopes)
    
    # The initial state: the start node with distance 0 and its set of visited nodes
    Q = deque([(start, 0, frozenset([start]))])
    visited = set()
    maxPath = 0
    
    i = 0
    while len(Q) > 0:
        i += 1
        current, dist, visited = Q.popleft()        
        
        # Whenever we reach the end, we update our currently longest path
        if current == end:
            if maxPath < dist:
                maxPath = dist
        
        
        for (n, ndist) in EDGES[current]:
            if n in G and n not in visited:
                Q.append((n, dist+ndist, visited | {n}))
        
    
    return maxPath


print(edgeBfs(start, end, True))
print(edgeBfs(start, end, False))



# It is possible to solve Part 2 with a BFS-based approach.
# However, exhaustive search like this are often better implemented
# as a DFS because of the memory requirements.
# edgeDfs() is only implemented for Part 2.

EDGES_WITHOUT_SLOPES = dict()
for c in CROSSINGS:
    EDGES_WITHOUT_SLOPES[c] = findEdges(c, False)

def edgeDfs(current, end, pathLen, visited):
    if current == end:
        return pathLen
    
    visited.add(current)
    
    maxPath = 0
    
    for (n, ndist) in EDGES_WITHOUT_SLOPES[current]:
        if n in G and n not in visited:
            maxPath = max(maxPath, edgeDfs(n, end, pathLen+ndist, visited))
            
    visited.discard(current)
    return maxPath


print(edgeDfs(start, end, 0, {start}))
