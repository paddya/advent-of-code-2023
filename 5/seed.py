import sys
from collections import defaultdict

blocks = [l for l in open(sys.argv[1]).read().split('\n\n')]

seeds, *blocks = blocks

seeds = [int(s) for s in seeds.removeprefix('seeds: ').split()]

# Just store all maps in a nested list
maps = [[] for _ in range(7)]

for i, b in enumerate(blocks):
    lines = b.split('\n')
    _, *mappings = lines
    maps[i] = []
    for l in mappings:
        dest, src, length = l.split()
        maps[i].append((int(dest), int(src), int(length)))
        

for m in maps:
    bounds = []
    for _, lb, length in m:
        bounds.append(lb)
        bounds.append(lb+length-1)
        
    bounds = list(sorted(bounds))
    for i in range(2, len(bounds), 2):
        if bounds[i] - bounds[i-1] != 1:
            print(bounds[i], bounds[i-1], bounds[i] - bounds[i-1])
        
        
def mapper(src, map):
    dest = src
    
    for rdest, rsrc, length in map:
        if rsrc <= src < rsrc + length:
            dest = rdest + (src - rsrc)
            break
    
    return dest

def mapSeed(src):
    dest = src
    for i, m in enumerate(maps):
        dest = mapper(dest, m)
        print(i, dest)
    return dest

def reverseMapper(dest, map):
    src = dest
    for i, (rdest, rsrc, length) in enumerate(map):
        if rdest <= dest < rdest + length:
            print('Rule ', i)
            return rsrc + (dest - rdest)

    
    print('No rule found')
    return src

def reverseMapSeed(dest):
    src = dest
    for m in reversed(maps):
        src = reverseMapper(src, m)
    return src


    
# lowest = 10e9
# for s in seeds:
#     s = mapSeed(s)
#     if s < lowest:
#         lowest = s

seedRanges = []
for i in range(0, len(seeds), 2):
    start, length = seeds[i], seeds[i+1]
    seedRanges.append((start, length))

def findMapping(index, mappings):
    for rdest, rsrc, length in mappings:
        if rsrc <= index < rsrc + length:
            return (rdest, rsrc, length)
    
    return None

def mapRange(range, mappings):
    start, rangeLen = range
    
    results = []
    
    lowestSrc = min(src for (_, src, _) in mappings)
    highestSrc = max(src+length for (_, src, length) in mappings)
    
    while rangeLen > 0:
        if start < lowestSrc:
            coveredRange = min(lowestSrc-start, rangeLen)

            results.append((start, coveredRange))
            start += coveredRange
            rangeLen -= coveredRange
            continue
        
        if start >= highestSrc:

            coveredRange = rangeLen

            results.append((start, coveredRange))
            start += coveredRange
            rangeLen -= coveredRange
            continue
        
        # Approach: find a mapping, then see how much of the range
        # we can cover with it, then find the next range
        curMapping = findMapping(start, mappings)
        
        if curMapping == None:
            print('No mapping found for start = ', start)
            break
        
        dest, src, length = curMapping
        
        coveredRange = min(length-(start-src), rangeLen)
        
        results.append((dest+(start-src), coveredRange))

        rangeLen -= coveredRange
        start += coveredRange
        
    return results
    

ranges = seedRanges
for i, m in enumerate(maps):
    newRanges = []
    for r in ranges:
        result = mapRange(r, m)
        newRanges = newRanges + result
    ranges = newRanges
    
        
print(min(dest for (dest, _) in ranges))    


    

