import sys
from collections import deque, defaultdict

# Map the current direction of the animal to its target direction if it encounters a tile
# Attention: player orientation is reversed from tile orientation!

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
PIPE_MAP = {
    'NORTH': {
        '|': 'NORTH',
        '-': None,
        'L': None, # wrong direction
        'J': None, # wrong direction
        '7': 'WEST',
        'F': 'EAST',
        '.': None
    },
    'SOUTH': {
        '|': 'SOUTH',
        '-': None,
        'L': 'EAST', # wrong direction
        'J': 'WEST', # wrong direction
        '7': None,
        'F': None,
        '.': None
    },
    'EAST': {
        '|': None,
        '-': 'EAST',
        'L': None, # wrong direction
        'J': 'NORTH',
        '7': 'SOUTH',
        'F': None,
        '.': None
    },
    'WEST': {
        '|': None,
        '-': 'WEST',
        'L': 'NORTH', # wrong direction
        'J': None,
        '7': None,
        'F': 'SOUTH',
        '.': None
    }
}


def printGrid(grid):
    for r in grid:
        for c in r:
            print(c, end='')
        print('')
        
def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

grid = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]

# Pad the grid with . to avoid detection for the borders
grid.insert(0, ['.' for _ in range(len(grid[1]))])
grid.append(['.' for _ in range(len(grid[1]))])

for row in grid:
    row.insert(0, '.')
    row.append('.')

WIDTH = len(grid[0])
HEIGHT = len(grid)

pipeNodes = set()

# Find start position and build set of all pipe nodes
startPosition = (-1, -1)
found = False
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == 'S':
            startPosition = (r, c)
        elif cell != '.':
            pipeNodes.add((r, c))
        
# Find neighbors of start node to get possible start directions

DIRECTIONS = {
    'WEST': (0, -1),
    'EAST': (0, 1),
    'NORTH': (-1, 0),
    'SOUTH': (1, 0),
}

directions = []

for direction, m in DIRECTIONS.items():
    neighbor = addTuple(startPosition, m)
    if neighbor in pipeNodes:
        r, c = neighbor
        tile = grid[r][c]
        if PIPE_MAP[direction][tile] != None:
            directions.append(direction)
        
        
# Replace start tile
TILE_MAP = {
    ('NORTH', 'SOUTH'): '|',
    ('SOUTH', 'NORTH'): '|',
    ('EAST', 'WEST'): '-',
    ('WEST', 'EAST'): '-',
    ('NORTH', 'EAST'): 'L',
    ('EAST', 'NORTH'): 'L',
    ('NORTH', 'WEST'): 'J',
    ('WEST', 'NORTH'): 'J',
    ('SOUTH', 'WEST'): '7',
    ('WEST', 'SOUTH'): '7',
    ('SOUTH', 'EAST'): 'F',
    ('EAST', 'SOUTH'): 'F',
}

START_DIRECTIONS = {
    '|': ['NORTH', 'SOUTH'],
    '-': ['EAST', 'WEST'],
    'L': ['NORTH', 'EAST'],
    'J': ['NORTH', 'WEST'],
    '7': ['SOUTH', 'WEST'],
    'F': ['SOUTH', 'EAST']
}

startR, startC = startPosition
startTile = TILE_MAP[tuple(directions)]
grid[startR][startC] = startTile

# Do BFS twice from the start position

def findMainLoop(start, orientations):
    visited = set()
    D = defaultdict(lambda: 10e9)
    D[start] = 0
    # Add both start positions to the queue
    Q = deque([(start, orientations[0]), (start, orientations[1])])
    
    while len(Q) > 0:
        pos, orientation = Q.popleft()
        visited.add(pos)
        
        #print('Popped', pos, ' facing ', orientation)
        
        # Find the neighbor based on the old orientaiton, it's guaranteed that there is one
        neighbor = addTuple(pos, DIRECTIONS[orientation])
        assert neighbor != None, 'There should be a valid neighbor!'
        
        r, c = neighbor
        
        neighborTile = grid[r][c]
        
        newOrientation = PIPE_MAP[orientation][neighborTile]
        neighborDistance = D[pos] + 1
        if neighborDistance < D[neighbor]:
            # print('Queuing neighbor', neighbor, newOrientation, neighborTile)
            Q.append((neighbor, newOrientation))
            D[neighbor] = neighborDistance
            
        
    return max(D.values()), visited

distances = {}


maxDistanceInLoop, mainLoopTiles = findMainLoop(startPosition, START_DIRECTIONS[startTile])
print(maxDistanceInLoop)
        
        
# Replace each grid tile with a 3x3 tile
# where each tile either represents ground or pipe

# | becomes
# .|.
# .|.
# .|.

# F becomes
# ...
# .F-
# .|.

def sourceIndex(idx):
    return idx // 3


def targetFields(pos):
    r, c = pos
    l = []
    for rr in range(3):
        for cc in range(3):
            l.append((3*r+rr, 3*c+cc))
            
    return l

expandedGrid = [['.' for _ in range(WIDTH*3)] for _ in range(HEIGHT*3)]

EXPANSIONS = {
    '.': [
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.'],
    ],
    '|': [
        ['.', '|', '.'],
        ['.', '|', '.'],
        ['.', '|', '.'],
    ],
    '-': [
        ['.', '.', '.'],
        ['-', '-', '-'],
        ['.', '.', '.']
    ],
    'F': [
        ['.', '.', '.'],
        ['.', 'F', '-'],
        ['.', '|', '.'],
    ],
    'L': [
        ['.', '|', '.'],
        ['.', 'L', '-'],
        ['.', '.', '.'],
    ],
    'J': [
        ['.', '|', '.'],
        ['-', 'J', '.'],
        ['.', '.', '.'],
    ],
    '7': [
        ['.', '.', '.'],
        ['-', '7', '.'],
        ['.', '|', '.']
    ]
}

# Fill the grid
for r in range(HEIGHT):
    for c in range(WIDTH):
        # Fill a 3x3 grid depending on the source cell
        source = grid[r][c]
        
        expansion = EXPANSIONS[source]
        
        for rr in range(3):
            for cc in range(3):
                expandedGrid[r*3+rr][c*3+cc] = expansion[rr][cc]
        
    
EXPANDED_HEIGHT = len(expandedGrid)
EXPANDED_WIDTH = len(expandedGrid[0])


# Implement a flood fill algorithm that finds all reachable nodes
def flood(start):
    Q = deque([start])
    # keep track of all filled nodes in the expanded grid
    visited = set()
    # keep track of all visited nodes in the source grid
    result = set()
    while len(Q) > 0:
        n = Q.popleft()
        r, c = n
        if n not in visited and expandedGrid[r][c] == '.':
            visited.add(n)
            result.add((sourceIndex(r), sourceIndex(c)))
            for m in DIRECTIONS.values():
                neighbor = addTuple(n, m)
                nr, nc = neighbor
                if 0 <= nr < EXPANDED_HEIGHT and 0 <= nc < EXPANDED_WIDTH:
                    Q.append(neighbor)
                
    
    # All nodes which are not colored are inside the main loop
    return WIDTH*HEIGHT-len(result)
            
  
print(flood((0, 0)))


# Inefficient initial solution, running BFS from any candidate node until it reaches the outside
# The efficient approach basically does the opposite        

# candidates = 0
# for r in range(1, len(grid)-1):
#     for c in range(1, len(grid[r])-1):
#         if (r, c) in mainLoopTiles:
#             continue
#         candidates += 0 if squeezyBFS((r,c)) else 1
        
#print(candidates)

def squeezyBFS(start):
    # For each start tile, expand it first into its target tiles and add all of them
    # If we find a path from any of the subtiles, we can assume the tile to be outside the main loop
    startNodes = targetFields(start)
    Q = deque(startNodes)
    visited = set(startNodes)
        
    while len(Q) > 0:
        current = Q.popleft()
        
        r, c = current
        
        # We reached the outside
        if (sourceIndex(r) == 0 or sourceIndex(c) == 0) or sourceIndex(r) == HEIGHT-1 or sourceIndex(c) == WIDTH-1:
            return True
        
        # The easy moves, find adjacent ground tiles
        for m in DIRECTIONS.values():
            neighbor = addTuple(current, m)
            nr, nc = neighbor

            if neighbor not in visited and 0 <= sourceIndex(nr) < HEIGHT and 0 <= sourceIndex(nc) < WIDTH and expandedGrid[nr][nc] == '.':
                Q.append(neighbor)
                visited.add(neighbor)
                
    return False