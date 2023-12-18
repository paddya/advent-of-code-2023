import sys
from collections import defaultdict

instructions = [l.split() for l in open(sys.argv[1]).read().split('\n')]

directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1)
}

dug = defaultdict(set)
G = set()

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])


def printGrid(G):
    min_x = min(c for (r,c) in G)
    max_x = max(c for (r,c) in G)
    min_y = min(r for (r,c) in G)
    max_y = max(r for (r,c) in G)
    print('WIDTH', max(c for (r, c) in G), min(c for (r,c) in G))
    print('HEIGHT', max(r for (r, c) in G), min(r for (r,c) in G))
    
    for r in range(min_y-2, max_y+2):
        for c in range(min_x-2, max_x+2):
            print('#' if (r, c) in G else '.', end='')
        print('')

current = (0, 0)
for instruction in instructions:
    direction, length = instruction[0], int(instruction[1])
    
    for _ in range(length):
        G.add(current)
        dug[current[0]].add(current[1])
        current = addTuple(current, directions[direction])
        
total = 0
def countInterior(G):
    min_x = min(c for (r,c) in G)
    max_x = max(c for (r,c) in G)
    min_y = min(r for (r,c) in G)
    max_y = max(r for (r,c) in G)
    print('WIDTH', max(c for (r, c) in G), min(c for (r,c) in G))
    print('HEIGHT', max(r for (r, c) in G), min(r for (r,c) in G))
    
    count = 0
    G2 = set()
    for r in range(min_y-1, max_y+1):
        isIn = False
        for c in range(min_x-1, max_x+1):
            if ((r, c) in G):
                if (r,c-1) not in G:
                    isIn = not isIn
            if (r, c) not in G and isIn:
                count += 1
                G2.add((r,c))
    
    return count, G2

count, interior = countInterior(G)

#printGrid(interior)
printGrid(interior | G)
print(count, len(G))
print(count+len(G))