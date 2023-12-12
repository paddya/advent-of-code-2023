import sys
from collections import deque
lines = [l for l in open(sys.argv[1]).read().split('\n')]

# Find all existing runs in the format (char, length) = (#, 3)
# Unused, I thought I needed this for part 1
def scan(space):
    cur = ''
    curLen = 0
    groups = []
    for c in space:
        if cur != c:
            if cur != '':
                groups.append((cur, curLen))
            curLen = 0
            cur = c
        curLen += 1
    groups.append((cur, curLen))    
    return groups

def match(groups, lengths):
    groupLengths = [l for (c, l) in groups if c == '#']
    return tuple(groupLengths) == tuple(lengths)

# Merge continuous groups
def merge(groups):
    result = []
    cur = ''
    curLen = 0
    for (c, length) in groups:
        if cur != c:
            if cur != '':
                result.append((cur, curLen))
            curLen = 0
            cur = c
        curLen += length
    result.append((cur, curLen))
    
    return result

# Used for part 1:
# - Find all the wildcard positions
# - Generate all numbers between 0 and (2^len(wildcards))-1
# - Set the wildcards based on the bits set in the given number
# - Validate
def solve(space, lengths):
    numWildcards = len([c for c in space if c == '?'])
    wildcardPositions = [i for i,c in enumerate(space) if c == '?']
    
    result = 0
    
    if numWildcards > 0:
        for i in range(2**numWildcards):
            copy = [c for c in space]
            for k, pos in enumerate(wildcardPositions):
                copy[pos] = '#' if (i & (1 << k)) > 0 else '.'
            groups = merge([(c, 1) for c in copy])
            if match(groups, lengths):
                result += 1
                
    return result


CACHE = dict()           
def solve_efficient(space, lengths, initialBlockSize=0):
    key = (space, lengths, initialBlockSize)
    if key in CACHE:
        return CACHE[key]
    
    # Terminate early if it's impossible for the remaining space to be enough for the missing blocks
    if len(space) + initialBlockSize < sum([x+1 for x in lengths])-1:
        CACHE[key] = 0
        return 0
    
    curBlockSize = initialBlockSize
    for idx, c in enumerate(space):
        # Keep increasing the current block
        if c == '#':
            curBlockSize += 1
        # If we have a block and/or are at the end of the string, terminate the current block
        if c == '.' or (idx == len(space)-1 and c == '#'):
            if curBlockSize > 0:
                if len(lengths) > 0 and curBlockSize == lengths[0]:
                    lengths = lengths[1:]
                    curBlockSize = 0
                else:
                    #print('Aborting!', curBlockSize, ' is larger than expected')
                    return 0
        # Recurse at wildcards, try to solve with both a . and a #
        if c == '?':
            withBlock = "#" + space[idx+1:]
            withoutBlock = "." + space[idx+1:]
            total = solve_efficient(withBlock, lengths, curBlockSize) + solve_efficient(withoutBlock, lengths, curBlockSize)
            CACHE[key] = total
            return total    

    # We only reach this if we are at the end of a string. A combination is only valid
    # if we have no more blocks left in our list
    if len(lengths) == 0:
        CACHE[key] = 1
        return 1
    else:
        CACHE[key] = 0
        return 0
    

# Blow up a line for part 2
def blow_up(space, lengths):
    return '?'.join([space]*5), tuple(lengths*5)

total = 0
total_p2 = 0

for l in lines:
    space, lengths = l.split(' ')
    lengths = tuple([int(l) for l in lengths.split(',')])
    total += solve_efficient(space, lengths)
    total_p2 += solve_efficient(*blow_up(space, lengths))

print(total)
print(total_p2)