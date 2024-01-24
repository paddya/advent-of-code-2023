import sys
from collections import deque, defaultdict
from heapq import heappush, heappop
from functools import cache

sys.setrecursionlimit(100000)

grid = [[c for c in row] for row in open(sys.argv[1]).read().split('\n')]

WIDTH = len(grid[0])
HEIGHT = len(grid)

G = dict()

for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        G[(r,c)] = cell

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
    


    
print(start, end)

mv = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0)
}

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
    

def edgeBfs(start, end, withSlopes):
    EDGES = dict()
    for c in CROSSINGS:
        EDGES[c] = findEdges(c, withSlopes)
    
    Q = deque([(start, 0, frozenset([start]))])
    visited = set()
    maxPath = 0
    D = defaultdict(int)
    D[start] = 0
    
    i = 0
    while len(Q) > 0:
        i += 1
        current, dist, visited = Q.popleft()
        r, c = current
        
        #print(current, visited, EDGES[current])
        
        if current == end:
            if maxPath < dist:
                print('Found path: ', dist)

                maxPath = dist
        
        
        for (n, ndist) in EDGES[current]:
            if n in G and n not in visited:
                Q.append((n, dist+ndist, visited | {n}))
        
    
    return maxPath
        

#print(edgeBfs(start, end, True))
#print(edgeBfs(start, end, False))
