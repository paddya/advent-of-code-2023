import sys
import re

from collections import defaultdict

instructions = open(sys.argv[1]).read().split(',')


def hash(instruction):
    current = 0
    for c in instruction:
        current += ord(c)
        current *= 17
        current %= 256
        
    return current
        
        
print(sum(hash(instruction) for instruction in instructions))

BOXES = defaultdict(list)

for instruction in instructions:
    label, op, focalLength = re.match('([A-z]+)(=|-)(\d+)?', instruction).groups()
    focalLength = int(focalLength) if not focalLength == None else None
    
    box = hash(label)
    lenses = BOXES[box]
    if op == "-":
        for i, (existingLabel, length) in enumerate(lenses):
            if existingLabel == label:
                BOXES[box] = lenses[:i] + lenses[i+1:]
                break

    if op == "=":
        replaced = False
        for i, (existingLabel, length) in enumerate(lenses):
            if existingLabel == label:
                BOXES[box] = lenses[:i] + [(label, focalLength)] + lenses[i+1:]
                replaced = True
                break
        if not replaced:
            BOXES[box].append((label, focalLength))

total_p2 = 0         
for box, lenses in BOXES.items():
    for i, (_, focalLength) in enumerate(lenses):
        total_p2 += (box+1)*(i+1)*focalLength
print(total_p2)