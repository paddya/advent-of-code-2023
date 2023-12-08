import sys
import re
from collections import defaultdict
import math

instructions, graph = [b for b in open(sys.argv[1]).read().split('\n\n')]
G = {}

for node in graph.split('\n'):
    node, left, right = re.findall('([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', node)[0]
    G[node] = (left, right)

currentNodes = [n for n in G.keys() if n.endswith('A')]
steps = 0

current = currentNodes[0]

numSteps = {}

for i, start in enumerate(currentNodes):
    steps = 0
    visited = set()
    current = start
    while not current.endswith('Z'):
        instruction = instructions[steps % len(instructions)]
        (l, r) = G[current]
        current = l if instruction == 'L' else r
        steps += 1
    numSteps[start] = steps
    
print(numSteps['AAA'])
print(math.lcm(*numSteps.values()))
    
