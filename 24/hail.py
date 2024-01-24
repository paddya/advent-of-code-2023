import sys
from itertools import combinations
import numpy as np
from z3 import *

lines = open(sys.argv[1]).read().split('\n')

hailstones = []

for l in lines:
    pos, velocity = l.split(' @ ')
    pos = tuple(map(int, pos.split(', ')))
    velocity = tuple(map(int, velocity.split(', ')))
    hailstones.append((pos, velocity))
    

BOUNDARIES = [200000000000000, 400000000000000] if sys.argv[1] != "example.txt" else [7, 27]

def intersect2d(s1, s2):
    #print('comparing', s1, s2)
    p1, p2 = s1[0], s2[0]
    v1, v2 = s1[1], s2[1]
    px1, px2 = p1[0], p2[0]
    vx1, vx2 = v1[0], v2[0]    
    
    py1, py2 = p1[1], p2[1]
    vy1, vy2 = v1[1], v2[1]
    
    a = np.array([[vx1, -vx2], [vy1, -vy2]])
    b = np.array([px2-px1, py2-py1])
    
    try:
        t1, t2 = np.linalg.solve(a, b)
        #print(t1, t1 >= 0, t2, t2 >= 0)
        if t1 >= 0 and t2 >= 0:
            xt1 = px1+t1*(vx1)
            yt1 = py1+t1*(vy1)
            
            if not (BOUNDARIES[0] <= xt1 <= BOUNDARIES[1]):
                return False
            if not (BOUNDARIES[0] <= yt1 <= BOUNDARIES[1]):
                return False
            
            return True
        return False
        
    except Exception as e:
        return False


total = 0
for s1, s2 in combinations(hailstones, 2):
    if intersect2d(s1, s2):
        total += 1
        
print(total)

# Pick three stones, and intersect each of them with the rock

h = hailstones[:3]

solver = Solver()
rx = Real('rx')
ry = Real('ry')
rz = Real('rz')

rvx = Real('rvx')
rvy = Real('rvy')
rvz = Real('rvz')

# Now add the 9 equations
p1, v1 = h[0]
p2, v2 = h[1]
p3, v3 = h[2]

solver = Solver()

for i, h in enumerate(hailstones):
    p, v = h
    t = Real(f't{i}')
    solver.add(rx + t*rvx == p[0] + t*v[0])
    solver.add(ry + t*rvy == p[1] + t*v[1])
    solver.add(rz + t*rvz == p[2] + t*v[2])

solver.check()
model = solver.model()
print(model)
print(model.eval(rx+ry+rz))

