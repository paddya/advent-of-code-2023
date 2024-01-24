from __future__ import annotations

import sys
from collections import defaultdict, deque

lines = open(sys.argv[1]).read().split('\n')

class Cube:
    def __init__(self, idx, min: tuple, max: tuple) -> None:
        self.idx = idx
        self.min = min
        self.max = max
        
    def supports(self, other: Cube):
        # print('Checking', self, other)
        xmin1, xmin2 = self.min[0], other.min[0]
        xmax1, xmax2 = self.max[0], other.max[0]
        ymin1, ymin2 = self.min[1], other.min[1]
        ymax1, ymax2 = self.max[1], other.max[1]
        
        if self.max[2] == other.min[2]-1:
            if (xmin2 <= xmin1 <= xmax2 or
                xmin2 <= xmax1 <= xmax2 or
                xmin1 <= xmin2 <= xmax1 or 
                xmin1 <= xmax2 <= xmax1):
                if (ymin2 <= ymin1 <= ymax2 or
                    ymin2 <= ymax1 <= ymax2 or
                    ymin1 <= ymin2 <= ymax1 or
                    ymin1 <= ymax2 <= ymax1):
                    return True
                
        return False
    
    def zmin(self):
        return self.min[2]    
    
    def zmax(self):
        return self.max[2]
    
    def moveDown(self):
        if self.min[2] == 1:
            return False
        self.min = (self.min[0], self.min[1], self.min[2]-1)
        self.max = (self.max[0], self.max[1], self.max[2]-1)
        return True
    
    def __repr__(self) -> str:
        return str(self.idx)
                
    def __str__(self) -> str:
        return f'{self.idx}'

CUBES = []    
ZINDEX = defaultdict(set)

#letters = 'ABCDEFGH'

for i, l in enumerate(lines):
    start, end = l.split('~')
    start = tuple(map(int, start.split(',')))
    end = tuple(map(int, end.split(',')))
    cube = Cube(i, start, end)
    CUBES.append(cube)
    ZINDEX[end[2]].add(cube)

anyMove = True
while anyMove:
    anyMove = False
    maxIndex = max(ZINDEX.keys())
    
    for i in range(maxIndex+1):
        toCheck = frozenset(ZINDEX[i])
        for c1 in toCheck:
            hasSupport = False
            while not hasSupport:
                for c2 in ZINDEX[c1.zmin() - 1]:
                    if c2.supports(c1):
                        hasSupport = True
                        break
                if not hasSupport:
                    oldZ = c1.zmax()
                    moved = c1.moveDown()
                    anyMove |= moved
                    if moved:
                        ZINDEX[oldZ].remove(c1)
                        ZINDEX[c1.zmax()].add(c1)
                    else:
                        break
            
SUPPORTED_BY = defaultdict(list)
SUPPORTING = defaultdict(list)

for c1 in CUBES:
    #print(c1)
    for c2 in ZINDEX[c1.zmin()-1]:
        if c2.supports(c1):
            SUPPORTED_BY[c1.idx].append(c2)
            SUPPORTING[c2.idx].append(c1)

total = 0
for c1 in CUBES:
    #print(c1, ' supports ', SUPPORTING[c1.idx])
    allSupportedSupportedByOthers = True
    for c2 in SUPPORTING[c1.idx]:
        if len(SUPPORTED_BY[c2.idx]) == 1:
            allSupportedSupportedByOthers = False
    if allSupportedSupportedByOthers:
        total += 1


def walkTree(start):
    Q = deque([start])
    fallen = set()

    while len(Q) > 0:
        current = Q.popleft()
        fallen.add(current)
        
        # For each neighbor, check whether it would fall if current falls
        for neighbor in SUPPORTING[current.idx]:
            hasSupport = False
            for supportedBy in SUPPORTED_BY[neighbor.idx]:
                if supportedBy in fallen:
                    continue
                hasSupport = True
            if not hasSupport:
                Q.append(neighbor)
        
    return len(fallen)-1

print(total)

total_p2 = 0
for c in CUBES:
    numFall = walkTree(c)
    total_p2 += numFall

print(total_p2)