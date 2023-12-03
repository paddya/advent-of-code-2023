import sys
from collections import defaultdict

# only 12 red cubes, 13 green cubes, and 14 blue
allowed = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


lines = [l.strip() for l in open(sys.argv[1])]

sum = 0
cubeSum = 0

for l in lines:
    [game, numbers] = l.split(': ')
    game = int(game.replace('Game ', ''))
    rounds = numbers.split(';')
    gamePossible = True
    colorMax = defaultdict(int)

    for r in rounds:
        colors = r.split(',')
        for c in colors:
            c = c.strip()
            (num, color) = c.split(' ')
            if int(num) > allowed[color]:
                gamePossible = False
            if int(num) > colorMax[color]:
                colorMax[color] = int(num)
    if gamePossible:
        sum += game
    cubeSum += colorMax['green'] * colorMax['red'] * colorMax['blue']

print(sum)  
print(cubeSum) 
