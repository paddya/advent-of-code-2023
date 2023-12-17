import sys
from copy import deepcopy
from itertools import pairwise

patterns = [p.split('\n') for p in open(sys.argv[1]).read().split('\n\n')]


def flip(pattern):
    result = [['?' for _ in range(len(pattern))] for _ in range(len(pattern[0]))]
    for r, row in enumerate(pattern):
        for c, cell in enumerate(row):
            result[c][r] = cell
            
    return [''.join(r) for r in result]

def printPattern(pattern, horizontal=-1, vertical=-1):
    for r, p in enumerate(pattern):
        if r == horizontal:
            print('-'*len(p))
        if vertical != -1:
            print(p[:vertical] + '|' + p[vertical:])
        else: print(p)
    

def findHorizontal(pattern):
    # Either the first or the last row MUST be part of a reflection if there is one
    # So we check them separately
    lastIndex = len(pattern)-1
    
    def findDuplicate(i):
        dups = []
        for j in range(len(pattern)):
            if i == j: continue
            if pattern[i] == pattern[j]:
                dups.append(j)
        return dups
    
    def isValidReflection(i, j):
        if (i - j + 1) % 2 != 0:
            return False
        upRange = range(i,j)
        downRange = range(j, i-1, -1)
        for (l,k) in zip(upRange, downRange):
            if l>=k:
                continue
            if pattern[l] != pattern[k]:
                return False
        return True
    
    firstDups = findDuplicate(0)
    lastDups = findDuplicate(lastIndex)
    
    candidates = []
    for d in firstDups:
        if isValidReflection(0, d):
            candidates.append(d // 2 + 1)
        
    for d in lastDups:
        if isValidReflection(d, lastIndex):
            candidates.append(d+(lastIndex-d)//2 + 1)
            
    return candidates


def smudgeVariants(pattern):
    variants = []
    p = [[c for c in row] for row in pattern]
    for r, row in enumerate(pattern):
        for c, cell in enumerate(row):
            variant = deepcopy(p)
            variant[r][c] = '#' if p[r][c] == '.' else '.'
            variants.append(((r,c), [''.join(r) for r in variant]))
            
    return variants
        
def find(p):
    candidates = []
    horizontal = findHorizontal(p)

    for h in horizontal:
        candidates.append((h, 'horizontal'))
    fp = flip(p)
    vertical = findHorizontal(fp)
    for v in vertical:
        candidates.append((v, 'vertical'))
    
    
    return candidates



total = 0
total_p2 = 0
for p in patterns:
    candidates = find(p)
    assert len(candidates) == 1
    idx, axis = candidates[0]
    
    if axis == 'vertical':
        total += idx
    if axis == 'horizontal':
        total += idx*100
        
    variants = smudgeVariants(p)
    found = False
    for (r, c), v in variants:
        candidates = find(v)
        for newIdx, newAxis in candidates:
            if (newIdx, newAxis) != (idx, axis) and newAxis != None:
                print(r, c, newAxis, newIdx)
                
                if newAxis == 'vertical':
                    total_p2 += newIdx
                if newAxis == 'horizontal':
                    total_p2 += newIdx*100
                
                found = True
                break
        if found:
            break
    printPattern(p)
    print('\n------------\n')
    printPattern(flip(p))
    print(len(variants), idx, axis)
    assert found
    print('\n================================\n\n')

print(total)
print(total_p2)