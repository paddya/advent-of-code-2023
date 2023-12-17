import sys
from collections import defaultdict

G = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]

WIDTH = len(G[0])
HEIGHT = len(G)


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def moveBeam(pos, direction):
    newPos = addTuple(pos, direction)
    r, c = newPos

    # Stop beams that are out of bounds
    if not (0 <= r < HEIGHT and 0 <= c < WIDTH):
        return []
    
    # Split beams that encounter a |
    dr, dc = direction
    if G[r][c] == '|' and dc != 0:
        return [(newPos, UP), (newPos, DOWN)]
    
    if G[r][c] == '-' and dr != 0:
        return [(newPos, LEFT), (newPos, RIGHT)]
    
    if G[r][c] == '\\':
        if dc == 1:
            return [(newPos, DOWN)]
        if dc == -1:
            return [(newPos, UP)]
        if dr == 1:
            return [(newPos, RIGHT)]
        if dr == -1:
            return [(newPos, LEFT)]
    if G[r][c] == '/':
        if dc == 1:
            return [(newPos, UP)]
        if dc == -1:
            return [(newPos, DOWN)]
        if dr == 1:
            return [(newPos, LEFT)]
        if dr == -1:
            return [(newPos, RIGHT)]
        
    return [(newPos, direction)]


def castBeam(beam):
    BEAMS = [beam]
    visited = set()

    visitedBy = set([((0, 0), (0, 1))])

    while len(BEAMS) > 0:
        aliveBeams = []
        
        for pos, direction in BEAMS:
            newBeams = moveBeam(pos, direction)
            for b in newBeams:
                if b in visitedBy:
                    continue
                aliveBeams.append(b)
                pos, _ = b
                visited.add(pos)
                visitedBy.add(b)
        BEAMS = aliveBeams
        
    return len(visited)
            
print(castBeam(((0, -1), (0, 1))))
    
START_BEAMS = []
# Generate starting from the left
for y in range(HEIGHT):
    START_BEAMS.append(((y, -1), (0, 1)))
    
# Generate starting from the right
for y in range(HEIGHT):
    START_BEAMS.append(((y, WIDTH), (0, -1)))
    
# Generate starting from the top
for x in range(WIDTH):
    START_BEAMS.append(((-1, x), (1, 0)))
    
# Generate starting from the bottom
for x in range(WIDTH):
    START_BEAMS.append(((HEIGHT, x), (-1, 0)))
    
curMax = 0
for b in START_BEAMS:
    result = castBeam(b)
    #print(b, result)
    if result > curMax:
        curMax = result
        
print(curMax)