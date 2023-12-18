import sys
from collections import defaultdict, deque
import math

rules, parts = open(sys.argv[1]).read().split('\n\n')

rules = rules.split('\n')
parts = parts.split('\n')

parsedRules = defaultdict(list)

def evaluate(param, operator, value):
    if operator == '<':
        return lambda part: part[param] < value
    elif operator == '>':
        return lambda part: part[param] > value
    return 

for r in rules:
    r = r.strip('}')
    key, mappings = r.split('{')
    
    for m in mappings.split(','):
        if ":" in m:
            condition, target = m.split(':')
            param, operator, value = condition[0], condition[1], condition[2:]
            parsedRules[key].append((evaluate(param, operator, int(value)), target, (param, operator, int(value))))
        else:
            parsedRules[key].append((lambda part: True, m, 'always true'))

parsedParts = []                

for p in parts:
    p = p.strip('{}')
    attributes = p.split(',')
    parsedPart = {}
    for a in attributes:
        key, value = a.split('=')
        parsedPart[key] = int(value)    
        
    parsedParts.append(parsedPart)
    

accepted = list()
for p in parsedParts:
    curRule = 'in'
    
    while curRule != 'R' and curRule != 'A':
        for i, (c, target, debug) in enumerate(parsedRules[curRule]):
            if c(p):
                curRule = target
                break
            else:
                continue
        
    if curRule == 'A':
        accepted.append(p)
    
total = 0    
for a in accepted:
    total += sum(p for p in a.values())
    
print(total)

def invert(condition):
    param, op, value = condition
    newOp = '>' if op == '<' else '<'
    return (param, newOp, value+1 if newOp == '<' else value-1)

def applyOperation(bounds, condition):
    newBounds = bounds.copy()
    param, op, value = condition
    if op == "<":
        newBounds[param] = (newBounds[param][0], min(value, newBounds[param][1]))
    else:
        # The lower bound is inclusive, so we need to add 1 to the value to get the proper new bound
        newBounds[param] = (max(newBounds[param][0], value+1), newBounds[param][1])

    return newBounds

def countPossibilities(rule, bounds):
    curRule = parsedRules[rule]
    if rule == 'A':
        result = math.prod((u-l) for l,u in bounds.values())
        return result
    
    if rule == 'R':
        return 0
    
    total = 0
    prevBounds = bounds.copy()
    for _, target, condition in curRule:
        if len(condition) == 3:
            newBounds = applyOperation(prevBounds, condition)
            prevBounds = applyOperation(prevBounds, invert(condition))
            total += countPossibilities(target, newBounds)
        else:
            total += countPossibilities(target, prevBounds)

            
    return total
    
    


print(countPossibilities('in', {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}))
