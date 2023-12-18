import sys
from collections import defaultdict

instructions = [l.split() for l in open(sys.argv[1]).read().split('\n')]



directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1)
}

dug = defaultdict(set)
G = set()
vertices = []

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def multiplyTuple(c, t):
    return (c*t[0], c*t[1])


def findVertices(instructions):
    current = (0, 0)
    vertices = [current]

    for instruction in instructions:
        direction, length = instruction[0], int(instruction[1])
        next = addTuple(current, multiplyTuple(length, directions[direction]))
        vertices.append(next)
        current = next
        
    return vertices[:-1]
        
# Apply shoelace formula
# A = 1/2 * abs((x1*y2 + ... + xn*y1) - (y1*x2 + ... + yn*x1))
def shoelace(vertices):
    A = 0
    numVertices = len(vertices)
    for i in range(numVertices):
        next = (i+1)%numVertices
        prev = (i-1)%numVertices
        p = 0.5*(vertices[i][1]) * (vertices[next][0] - vertices[prev][0])
        A += p
    return int(A)

def perimeter(instructions):
    return sum(int(x) for (_, x, _) in instructions)

print(shoelace(findVertices(instructions))+perimeter(instructions)//2+1)

# dig: 0 means R, 1 means D, 2 means L, and 3 means U.
p2Instructions = []
p2Map = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}
for instruction in instructions:
    _, _, hex = instruction
    hex = hex.strip("#()")
    length, direction = hex[:5], hex[5:]
    p2Instructions.append((p2Map[direction], int(length, 16), ""))
    
print(shoelace(findVertices(p2Instructions))+perimeter(p2Instructions)//2+1)




