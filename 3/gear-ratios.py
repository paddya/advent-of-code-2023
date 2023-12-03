import sys

lines = [l for l in open(sys.argv[1]).read().split('\n')]

G = [['.' for _ in range(len(lines[0]))] for _ in range(len(lines))]

WIDTH = len(lines[0])
HEIGHT = len(lines)

NUM_IDX = 0

# General idea: Collect all numbers and all gears into separate lists and store information about their
# location (and length for numbers). Each number is assigned an index to disambiguate duplicate
# numbers for Part 2. We then write a new grid G which for each cell contains either the index
# of the number it is occupied by, or a symbol.
# We can then iterate over all the numbers or all the gears and perform adjacency checks on G.

allNumbers = []
numbersByIndex = {}
allGears = []

# Check if there are vertical numbers
# for c in range(len(lines[0])):
#     for r in range(len(lines)):
#         if r == 0:
#             continue
#         if lines[r][c].isdigit() and lines[r-1][c].isdigit():
#             print('Found vertical number', r, c)

# Scan each line for numbers
for r, l in enumerate(lines):
    numberBuffer = []
    for c, symbol in enumerate(l):
        if symbol.isdigit():
            numberBuffer.append(symbol)
        # We need to handle the edge case if the line ends in a number
        if not symbol.isdigit() or c == WIDTH-1:
            # If we have something in numberBuffer, write it to the grid and clear the buffer
            if len(numberBuffer) > 0:
                # There are two cases:
                #   1. We are in the middle of the line and we just encountered a symbol
                #      In that case, we set endIdx to the current column
                #   2. We are at the end of a line and the line ended in a number
                #      We set endIdx to WIDTH (essentially adding 1)
                # Later, we use endIdx a the stop index for range() to write G
                # and to write the number to allNumbers (subtracting 1 to get the proper index)
                endIdx = c if not symbol.isdigit() else WIDTH
                number = ''.join(numberBuffer)
                # Take the end index, and move len(number) to the left
                startIdx = endIdx-len(number)
                
                for cc in range(startIdx, endIdx):
                    G[r][cc] = str(NUM_IDX)
                
                allNumbers.append((number, r, startIdx, endIdx-1, NUM_IDX))
                numbersByIndex[NUM_IDX] = int(number)
                numberBuffer = []
                NUM_IDX += 1
            
            # Now, check if we need to to write the symbol to the grid
            if symbol != '.' and not symbol.isdigit():
                G[r][c] = symbol
                
            if symbol == '*':
                allGears.append((r, c))
        
                

m = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Find numbers adjacent to a symbol
sum = 0
for number, row, start, end, _ in allNumbers:
    # if number != "866":
    #     continue
    hasSymbol = False
    for mr, mc in m:
        # The longest number is three digits long, so we can just check all directions from the left and the right of the number
        sr = row+mr
        sc = start+mc
        
        er = row+mr
        ec = end+mc
        
        if 0 <= sr < HEIGHT and 0 <= sc < WIDTH:
            if not G[sr][sc].isnumeric() and G[sr][sc] != '.':
                hasSymbol = True
                break
              
        if 0 <= er < HEIGHT and 0 <= ec < WIDTH:
            if not G[er][ec].isnumeric() and G[er][ec] != '.':
                hasSymbol = True
                break

    if hasSymbol:
        sum += int(number)
    # else:
    #     print(number, row, start, end, hasSymbol)
            
print(sum)


# Find gears with two adjacent numbers
gearSum = 0
for r, c in allGears:
    # if number != "866":
    #     continue
    hasSymbol = False
    adjacentNumbers = set()
    #print('Checking', r, c)
    for mr, mc in m:
        # The longest number is three digits long, so we can just check all directions from the left and the right of the number
        rr = r+mr
        cc = c+mc
        
        if 0 <= rr < HEIGHT and 0 <= cc < WIDTH:
            if G[rr][cc].isnumeric():
                adjacentNumbers.add(G[rr][cc])
              
    if len(adjacentNumbers) == 2:
        numbers = list(adjacentNumbers)
        gearSum += numbersByIndex[int(numbers[0])]*numbersByIndex[int(numbers[1])]
    
print(gearSum)