import sys
from collections import deque, Counter, defaultdict
from scipy import interpolate

G = [[c for c in row] for row in open(sys.argv[1]).read().split()]

numSteps = 64

WIDTH = len(G[0])
HEIGHT = len(G)

# Find start node

start = (-1, -1)
for r, row in enumerate(G):
    for c, cell in enumerate(row):
        if cell == 'S':
            start = (r,c)
            break


def printGrid(G, visited):
    for r, row in enumerate(G):
        for c, cell in enumerate(row):
            print(cell if not (r,c) in visited else 'O', end='')
        print('')
       

def bfs(start, numSteps):      
    Q = deque([(start, numSteps)])
    visited = set()
    exactly = set()

    mv = [(-1, 0), (1, 0), (0, -1), (0, 1)]     
    while len(Q) > 0:
        current, remaining = Q.popleft()
        r, c = current
        if remaining > 0:
            for (mr, mc) in mv:
                rr = (r+mr)
                cc = (c+mc)
                n = ((rr,cc), remaining-1)
                if G[rr % HEIGHT][cc % WIDTH] != '#' and n not in visited :
                    Q.append(n)
                    visited.add(n)
        else:
            exactly.add(current)
    return len(exactly)

a0 = bfs(start, 65)
a1 = bfs(start, 65+131)
a2 = bfs(start, 65+262)

f = interpolate.interp1d(x=[0, 1, 2], y=[a0, a1, a2], kind='quadratic', fill_value='extrapolate')

print(int(f(202300)))