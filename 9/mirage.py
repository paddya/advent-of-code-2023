import sys
from itertools import pairwise
from collections import deque

lines = [deque([int(k) for k in l.split()]) for l in open(sys.argv[1]).read().split('\n')]

def findAllSubsequences(sequence):
    allSeqs = [sequence]
    
    while not all(s == 0 for s in sequence):
        newSeq = deque([s2-s1 for (s1, s2) in pairwise(sequence)])
        allSeqs.append(newSeq)
        sequence = newSeq
        
    return allSeqs

def predictValues(sequences):
    for i in range(len(sequences)-1, 0, -1):
        toAdd = sequences[i][-1]
        lastElem = sequences[i-1][-1]
        sequences[i-1].append(lastElem+toAdd)
        
    return sequences

def predictPreviousValues(sequences):
    for i in range(len(sequences)-1, 0, -1):
        toSub = sequences[i][0]
        firstElem = sequences[i-1][0]
        sequences[i-1].appendleft(firstElem-toSub)
        
    return sequences

total = 0
total2 = 0
for l in lines:
    subSeqs = findAllSubsequences(l)
    newVals = predictValues(subSeqs)
    p2Vals = predictPreviousValues(newVals)
    total += newVals[0][-1]
    total2 += p2Vals[0][0]
    
print(total)
print(total2)