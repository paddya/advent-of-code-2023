
import sys
import re



lines = [l for l in open(sys.argv[1]).read().split('\n')]


numMap = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

def mapNumber(num: str):
    if num.isnumeric():
        return num
    else:
        return numMap[num]
    
def solve_p1(lines):
    sum = 0

    for l in lines:
        nums = re.findall("\d", l)
        num = int(mapNumber(nums[0]) + mapNumber(nums[len(nums)-1]))
        sum += num
    return sum

def solve_p2(lines):
    sum = 0

    for l in lines:
        # Some magic to handle overlapping numbers with a lookahead
        # See https://stackoverflow.com/a/5616910/11745846
        nums = re.findall("(?=(\d|one|two|three|four|five|six|seven|eight|nine))", l)
        num = int(mapNumber(nums[0]) + mapNumber(nums[len(nums)-1]))
        sum += num
    return sum
    
print(solve_p1(lines)) 
print(solve_p2(lines)) 