import sys
from collections import defaultdict, deque
import math

lines = open(sys.argv[1]).read().split('\n')

HIGH = 1
LOW = 0
# TODO: Instead of calling receive() on the output directly, return a list of pulses

class FlipFlop:
    def __init__(self, name) -> None:
        self.name = name
        self.on = False
        self.outputs = []
        self.inputs = {}
        pass
    
    def receive(self, name, pulse):
        if pulse == LOW:
            if self.on:
                self.on = False
                return self.send(LOW)
            else:
                self.on = True
                return self.send(HIGH)
        return []
    
    def send(self, pulse):
        return [(o.name, self.name, pulse) for o in self.outputs]
            
    def __str__(self) -> str:
        return '{name} -> {outputs}'.format(name=self.name, outputs=', '.join(map(lambda o: o.name, self.outputs)))
          
    def __repr__(self) -> str:
        return self.__str__()  

        
class Conjunction:
    def __init__(self, name) -> None:
        self.name = name
        self.outputs = []
        self.inputs = dict()
        pass
    
    def __str__(self) -> str:
        return '{name} -> {outputs}'.format(name=self.name, outputs=', '.join(map(lambda o: o.name, self.outputs)), inputs=', '.join(self.inputs.keys()))
 
    def __repr__(self) -> str:
        return self.__str__()
    
    def receive(self, name, pulse):
        self.inputs[name] = pulse
        return self.send()
    
    def send(self):
        pulse = LOW if all(p == HIGH for p in self.inputs.values()) else HIGH
        return [(o.name, self.name, pulse) for o in self.outputs]

    
class Broadcaster:
    def __init__(self, name) -> None:
        self.name = name
        self.outputs = []
        self.inputs = {}
        pass
    
    def receive(self, name, pulse):
        return [(o.name, self.name, pulse) for o in self.outputs]

    
    def __str__(self) -> str:
        return '{name} -> {outputs}'.format(name=self.name, outputs=', '.join(map(lambda o: o.name, self.outputs)))
 
    def __repr__(self) -> str:
        return self.__str__()
    
class Untyped:
    def __init__(self, name) -> None:
        self.name = name
        self.outputs = []
        self.inputs = {}
        pass
    
    def receive(self, name, pulse):
        return []

    
    def __str__(self) -> str:
        return '{name} -> {outputs}'.format(name=self.name, outputs=', '.join(map(lambda o: o.name, self.outputs)))
 
    def __repr__(self) -> str:
        return self.__str__()
    

ELEMS = dict()
INPUTS = defaultdict(list)

# First pass, create all the correct types
for l in lines:
    name, outputs = l.split(' -> ')
    outputs = outputs.split(', ')
    name = name[1:] if name[0] == '%' or name[0] == '&' else name
    if l.startswith('%'):
        ELEMS[name] = FlipFlop(name)
    elif l.startswith('&'):
        ELEMS[name] = Conjunction(name)
    else:
        ELEMS[name] = Broadcaster(name)
        
    for o in outputs:
        # Will be overriden if we later find it
        if not o in ELEMS:
            ELEMS[o] = Untyped(o)
        INPUTS[o].append(name)
        



# Second pass, properly map the outputs and inputs
for l in lines:
    name, outputs = l.split(' -> ')
    
    name = name[1:] if name[0] == '%' or name[0] == '&' else name
    outputs = outputs.split(', ')
    ELEMS[name].outputs = [ELEMS[o] for o in outputs if o in ELEMS]

    for input in INPUTS[name]:
        ELEMS[name].inputs[input] = LOW

pulses = [0, 0]
i = 0

TARGET_INPUTS = INPUTS[INPUTS['rx'][0]]
FIRST_RESULTS = {}

# General approach
# For part 1, we just implement the digital logic and count all the pulses.
# For part 2, we exploit the structure of the circuit (see graph.svg)
# There is only one conjunction feeding into rx (vf) and all the inputs
# of that conjunction are fed by one of four sub-circuits.
# vf will send a low pulse once all four sub-circuits send a high pulse
# at the same time. Since all four sub-circuits emit a high pulse
# periodically, we just need to find the LCM of the product of the
# period lengths.

found = False
while not found:
    i += 1
    Q = deque([('broadcaster', 'button', LOW)])
    
    while len(Q) > 0:
        target, source, pulse = Q.popleft()
        if source in TARGET_INPUTS and pulse == HIGH:
            FIRST_RESULTS[source] = i

            
        if len(FIRST_RESULTS) == len(TARGET_INPUTS):
            found = True
            break
        
        pulses[pulse] += 1
        result = ELEMS[target].receive(source, pulse)
        for r in result:
            Q.append(r)
    if i == 1000:
        print(math.prod(pulses))

    # numTrue = len([True for e in ELEMS.values() if isinstance(e, FlipFlop) and e.on])
    # print(i, numTrue)


print(math.lcm(*FIRST_RESULTS.values()))
