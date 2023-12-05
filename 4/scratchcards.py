import sys
from collections import defaultdict
lines = [l for l in open(sys.argv[1]).read().split('\n')]

numCards = defaultdict(int)
wmap = {}
omap = {}

total = 0
for l in lines:
    c, cards = l.split(': ')
    winning, own = cards.split(' | ')
    winning = set([int(c.strip()) for c in winning.strip().split(' ') if c.strip().isnumeric()])
    own = set([int(c.strip()) for c in own.strip().split(' ') if c.strip().isnumeric()])
    
    numWinning = len(winning & own)
    exp = numWinning-1
    total += 2**exp if exp >= 0 else 0
    
    gameNo = int(c.removeprefix('Card').strip())
    numCards[gameNo] += 1
    wmap[gameNo] = winning
    omap[gameNo] = own
    
    for i in range(gameNo+1, gameNo + numWinning+1):
        numCards[i] += numCards[gameNo]
        #print(gameNo, ' winning ', numCards[gameNo], ' copies of ', i)

        #print(numCards)
    
    #print('======')
print(total)
print(sum([v for v in numCards.values()]))
