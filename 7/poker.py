import sys
from collections import Counter
import functools

hands = [l.split() for l in open(sys.argv[1]).read().split('\n')]


# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
CARDS = {'A': 0, 'K': 1, 'Q': 2, 'J': 3, 'T': 4, '9': 5, '8': 6, '7': 7, '6': 8, '5': 9, '4': 10, '3': 11, '2': 12}
JOKER_CARDS = {'A': 0, 'K': 1, 'Q': 2, 'T': 3, '9': 4, '8': 5, '7': 6, '6': 7, '5': 8, '4': 9, '3': 10, '2': 11, 'J': 12}

TYPES = {'FIVE': 0, 'FOUR': 1, 'FULL_HOUSE': 2, 'THREE': 3, 'TWO_PAIR': 4, 'ONE_PAIR': 5, 'HIGH_CARD': 6}

def getType(card):
    counter = Counter(card)
    
    maxValue = max(counter.values())
    minValue = min(counter.values())
    
    valCounter = Counter(counter.values())
    
    if maxValue == 5:
        return 'FIVE'
    elif maxValue == 4:
        return 'FOUR'
    elif maxValue == 3:
        if minValue == 2:
            return 'FULL_HOUSE'
        else:
            return 'THREE'
    elif maxValue == 2:
        if valCounter[2] == 2:
            return 'TWO_PAIR'
        else:
            return 'ONE_PAIR'
    
    return 'HIGH_CARD'

def getTypeWithJoker(hand, debug=False):
    counter = Counter(hand)
    
    maxValue = 0
    maxCard = ''
    minValue = 6
    
    for c, count in counter.items():
        t = CARDS[c]
        if c == 'J':
            continue
        if (count > maxValue) or (count == maxValue and t < JOKER_CARDS[maxCard]):
            maxValue = count
            maxCard = c
        
        if (count < minValue) or (count == minValue and t > JOKER_CARDS[maxCard]):
            minValue = count
    
    if maxCard == '':
        maxCard = 'A'
        counter['A'] = 0
        
    if 'J' in counter:
        counter[maxCard] += counter['J']
        counter['J'] = 0
    
    valCounter = Counter(counter.values())
    
    maxValue = max(counter.values())
    minValue = min(c for c in counter.values() if c > 0)
    
    
            
    if maxValue == 5:
        return 'FIVE'
    elif maxValue == 4:
        return 'FOUR'
    elif maxValue == 3:
        if minValue == 2:
            return 'FULL_HOUSE'
        else:
            return 'THREE'
    elif maxValue == 2:
        if valCounter[2] == 2:
            return 'TWO_PAIR'
        else:
            return 'ONE_PAIR'
    
    return 'HIGH_CARD'

def sortedCmp(h1, h2):
    for c1, c2 in zip(h1, h2):
        r1, r2 = CARDS[c1], CARDS[c2]
        if r1 != r2:
            return r2-r1
    
    return 0

def sortedJokerCmp(h1, h2):
    for c1, c2 in zip(h1, h2):
        r1, r2 = JOKER_CARDS[c1], JOKER_CARDS[c2]
        if r1 != r2:
            return r2-r1
    
    return 0

def cmpCards(p1, p2):
    c1, _ = p1
    c2, _ = p2
    r1, r2 = TYPES[getType(c1)], TYPES[getType(c2)]
    
    
    # Ranks are lower when higher :D
    if r1 != r2:
        return r2 - r1

    return sortedCmp(c1, c2)

def cmpCardsWithJoker(p1, p2):
    c1, _ = p1
    c2, _ = p2
    t1 = getTypeWithJoker(c1)
    t2 = getTypeWithJoker(c2)
    r1, r2 = TYPES[t1], TYPES[t2]
    
    
    # Ranks are lower when higher :D
    if r1 != r2:
        return r2 - r1

    return sortedJokerCmp(c1, c2)

sortedHands = sorted(hands, key=functools.cmp_to_key(cmpCards))

#print(sortedHands)
total = 0
for i, (hand, bid) in enumerate(sortedHands):
    total += (i+1) * int(bid)
    
print(total)

sortedJokerHands = sorted(hands, key=functools.cmp_to_key(cmpCardsWithJoker))


total = 0
for i, (hand, bid) in enumerate(sortedJokerHands):
    total += (i+1) * int(bid)
    oldHand = getType(hand)
    newHand = getTypeWithJoker(hand)
    
    print(hand, getTypeWithJoker(hand), i+1, ' JOKER!' if 'J' in hand else '', bid)
    
print(total)