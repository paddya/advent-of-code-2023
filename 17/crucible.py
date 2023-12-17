import sys
from heapq import heapify, heappop, heappush
from dataclasses import dataclass, field


grid = [[int(c) for c in l] for l in open(sys.argv[1]).read().split('\n')]

WIDTH = len(grid[0])
HEIGHT = len(grid)

G = dict()
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        G[complex(c,r)] = cell
        
@dataclass(order=True, eq=True, frozen=True)
class State:
    pos: complex = field(compare=False, hash=True)
    direction: complex = field(compare=False, hash=True)
    numMovesInDirection: int

def findNeighbors(totalHeatLoss, state: State):
    neighbors = []
    
    # Continue straight forward
    if state.numMovesInDirection < 3:
        newPos = state.pos + state.direction
        if newPos in G:
            newState = State(newPos, state.direction, state.numMovesInDirection+1)
            neighbors.append((totalHeatLoss+G[newPos], newState))
    
    # Turn right: direction * i
    turnedRight = state.direction * complex(0, 1)
    newPos = state.pos + turnedRight
    if newPos in G:
        neighbors.append((totalHeatLoss+G[newPos], State(newPos, turnedRight, 1)))
        
    turnedLeft = state.direction * complex(0, -1)
    newPos = state.pos + turnedLeft
    if newPos in G:
        neighbors.append((totalHeatLoss+G[newPos], State(newPos, turnedLeft, 1)))
        
    return neighbors
        
def findUltraNeighbors(totalHeatLoss, state: State):
    neighbors = []
    
    # Continue straight forward
    if state.numMovesInDirection < 10:
        newPos = state.pos + state.direction
        if newPos in G:
            newState = State(newPos, state.direction, state.numMovesInDirection+1)
            neighbors.append((totalHeatLoss+G[newPos], newState))
    
    if state.numMovesInDirection >= 4:
        # Turn right: direction * i
        turnedRight = state.direction * complex(0, 1)
        newPos = state.pos + turnedRight
        if newPos in G:
            neighbors.append((totalHeatLoss+G[newPos], State(newPos, turnedRight, 1)))
        
        # Turn left: direction * -i
        turnedLeft = state.direction * complex(0, -1)
        newPos = state.pos + turnedLeft
        if newPos in G:
            neighbors.append((totalHeatLoss+G[newPos], State(newPos, turnedLeft, 1)))
        
    return neighbors




#### PART 1

# We only need to visit each block at most once in each direction
visited = set()
# State (totalHeatLoss, pos, direction, numMovesInDirection)
start = (0, State(pos=complex(0,0), direction=complex(0, 1), numMovesInDirection=0))

Q = list([start])
while len(Q) > 0:    
    totalHeatLoss, state = heappop(Q)
        
    if state.pos.imag == HEIGHT-1 and state.pos.real == WIDTH-1:
        print(totalHeatLoss)
        break
    
    neighbors = findNeighbors(totalHeatLoss, state)
    for priority, newState in neighbors:
        if not newState in visited:
            visited.add(newState)
            heappush(Q, (priority, newState))
            
    

### PART 2

start2 = (0, State(pos=complex(0,0), direction=complex(1, 0), numMovesInDirection=0))
    

Q = list([start, start2])
visited = set()

minDistance = 10e9

while len(Q) > 0:    
    totalHeatLoss, state = heappop(Q)
        
    if state.pos.imag == HEIGHT-1 and state.pos.real == WIDTH-1 and state.numMovesInDirection >= 4:
        minDistance = min(minDistance, totalHeatLoss)
        print('Found end', totalHeatLoss, state)
        break
    
    neighbors = findUltraNeighbors(totalHeatLoss, state)
    for priority, newState in neighbors:
        if not newState in visited:
            visited.add(newState)
            heappush(Q, (priority, newState))
            
print(minDistance)
    
    
    
