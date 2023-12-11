import sys

grid = [[c for c in r] for r in open(sys.argv[1]).read().split('\n')]

HEIGHT = len(grid)
WIDTH = len(grid[0])

galaxies = []
emptyRows = set()

emptyRowPrefixSum = []

anyInCol = [0 for _ in range(WIDTH)]

prevRow = 0
for r, row in enumerate(grid):
    anyInRow = False
    for c, cell in enumerate(row):
        if cell == '#':
            galaxies.append((r, c))
            anyInRow = True
            anyInCol[c] = 1
    
    cur = prevRow+1 if not anyInRow else prevRow
    emptyRowPrefixSum.append(cur)
    prevRow = cur
    
        

emptyColPrefixSum = [sum(anyInCol[:i+1]) for i in range(len(anyInCol))]

def distance(p1, p2, expansionFactor):
    p1_1, p1_2 = p1
    p2_1, p2_2 = p2
    numEmptyCols = countEmptyColumns(p1_2, p2_2)
    numEmptyRows = countEmptyRows(p1_1, p2_1)
    dy = abs(p1_1-p2_1)
    dx = abs(p1_2-p2_2)
    return dy+dx-numEmptyCols+numEmptyCols*expansionFactor-numEmptyRows+numEmptyRows*expansionFactor

def countEmptyColumns(x1, x2):
    return abs(emptyColPrefixSum[x1]-emptyColPrefixSum[x2])

def countEmptyRows(y1, y2):
    return abs(emptyRowPrefixSum[y1]-emptyRowPrefixSum[y2])


distances = []
total = 0
total_2 = 0
for g1 in galaxies:
    for g2 in galaxies:
        if g1 >= g2:
            continue
        
        total += distance(g1, g2, 2)
        total_2 += distance(g1, g2, 1000000)
        
print(total)
print(total_2)