import sys
import math

lines = [l for l in open(sys.argv[1]).read().split('\n')]

_, *srcTimes = lines[0].split()
_, *srcDistances = lines[1].split()

times = list(map(int, srcTimes))
distances = list(map(int, srcDistances))

# d < (t1)*(t-t1) <=> d < t1*t - t1^2
# 0 = -t1^2 + t1*t - d
# t1,2 = (-t +- sqrt(t^2 - 4*(-1)*(-d))/(-2))
def simulateRace(t, d):
    domain = t**2 - 4*(-1)*(-d)
    t1 = math.ceil((-t + math.sqrt(t**2 - 4*d))/(-2))
    t2 = math.floor((-t - math.sqrt(t**2 - 4*d))/(-2))
    
    return t2-t1+1

result = 1
for t, d in zip(times, distances):
    result *= simulateRace(t, d)

print(result)


p2_time = int(''.join(srcTimes))
p2_distance = int(''.join(srcDistances))

print(simulateRace(p2_time, p2_distance))


