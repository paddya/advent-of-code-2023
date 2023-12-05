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

    maps[i].sort(key=lambda x: x[1])
    
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
    return dest

    
lowest = 10e9
for s in seeds:
    s = mapSeed(s)
    if s < lowest:
        lowest = s
        
print(lowest)

seedRanges = []
for i in range(0, len(seeds), 2):
    start, length = seeds[i], seeds[i+1]
    seedRanges.append((start, length))

# Assumption: mappings are sorted
def findNextHigherMapping(index, mappings):
    for (dest, src, length) in mappings:
        if src > index:
            return (dest, src, length)
    return None
        

def findMapping(index, mappings):
    for rdest, rsrc, length in mappings:
        if rsrc <= index < rsrc + length:
            return (rdest, rsrc, length)
    
    return None

def mapRange(range, mappings):
    start, rangeLen = range
    
    results = []
    
    while rangeLen > 0:        
        # Approach: find a mapping, then see how much of the range
        # we can cover with it, then find the next range
        curMapping = findMapping(start, mappings)
        
        # Handle all edge cases where we don't actually find a mapping
        # Also handles cases where the gap is in the middle 
        if curMapping == None:
            nextHigher = findNextHigherMapping(start, mappings)
            # If there is no higher mapping, we can just cover the rest of the range 
            if nextHigher == None:
                coveredRange = rangeLen

                results.append((start, coveredRange))
                start += coveredRange
                rangeLen -= coveredRange
                continue
            else:
                (_, nsrc, _) = nextHigher

                # We can at most cover the gap between start and the start of the next higher interval
                coveredRange = min(nsrc-start, rangeLen)

                results.append((start, coveredRange))
                start += coveredRange
                rangeLen -= coveredRange
                continue
        
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
    

