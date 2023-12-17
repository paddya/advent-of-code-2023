import sys
from copy import deepcopy

G = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]
G2 = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]

WIDTH = len(G[0])
HEIGHT = len(G)

def printGrid(G):
    for r in G:
        print(''.join(r))

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def tiltNorth(G):
    W = len(G[0])
    H = len(G)
    
    for _ in range(H):
        cont = False
        for r in range(H):
            for c in range(W):
                if G[r][c] == 'O' and r > 0 and G[r-1][c] == '.':
                    G[r-1][c] = 'O'
                    G[r][c] = '.'
                    cont = True
        if not cont:
            break
                    
    return G

def weight(G):
    total = 0
    for r, row in enumerate(G):
        for c in row:
            if c == 'O':
                total += HEIGHT - r   
    return total  

# 1 2  => 3 1
# 3 4     4 2
# Rotate clockwise
def rotate(G):
    H = len(G[0])
    W = len(G)
    G2 = [['.' for _ in range(W)] for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            G2[c][W-r-1] = G[r][c]    
            
    return G2

def cycle(G):
    for _ in range(4):
        G = tiltNorth(G)
        G = rotate(G)
    return G

print(weight(tiltNorth(G)))

def REPR(G):    
    return frozenset([(r, c) for r in range(len(G)) for c in range(len(G[0])) if G[r][c] == 'O'])

Gx = G2
CACHE = dict()
WEIGHT_CACHE = dict()
i = 0
target = 1000000000
while i < target:
    # Figure out when it repeats
    repr = REPR(Gx)
    if repr in CACHE:
        cycleLength = i-CACHE[repr]
        
        numIterations = ((target - i) // cycleLength)
        skipTo = i + numIterations*cycleLength
        numCycles = target - skipTo

        print('Found cycle of length', cycleLength, ' at ', i, 'getting to ', skipTo, ' -- leaving', numCycles, ' cycles')

        print(WEIGHT_CACHE[CACHE[repr]+numCycles])
        break

        
    CACHE[REPR(Gx)] = i
    WEIGHT_CACHE[i] = weight(Gx)
    Gx = cycle(Gx)
    i += 1
