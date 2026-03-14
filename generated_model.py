from z3 import *
import random

rows = 5
cols = 5
T = 10

opt = Optimize()

x0 = [Int('x0_'+str(t)) for t in range(T)]
y0 = [Int('y0_'+str(t)) for t in range(T)]
b0 = [Real('b0_'+str(t)) for t in range(T)]
charge0 = [Bool('charge0_'+str(t)) for t in range(T)]
wait0 = [Int('wait0_'+str(t)) for t in range(T)]

x1 = [Int('x1_'+str(t)) for t in range(T)]
y1 = [Int('y1_'+str(t)) for t in range(T)]
b1 = [Real('b1_'+str(t)) for t in range(T)]
charge1 = [Bool('charge1_'+str(t)) for t in range(T)]
wait1 = [Int('wait1_'+str(t)) for t in range(T)]

x2 = [Int('x2_'+str(t)) for t in range(T)]
y2 = [Int('y2_'+str(t)) for t in range(T)]
b2 = [Real('b2_'+str(t)) for t in range(T)]
charge2 = [Bool('charge2_'+str(t)) for t in range(T)]
wait2 = [Int('wait2_'+str(t)) for t in range(T)]

xc = [Int('xc_'+str(t)) for t in range(T)]
yc = [Int('yc_'+str(t)) for t in range(T)]

opt.add(x0[0] == 0)
opt.add(y0[0] == 0)
opt.add(b0[0] == 5)

opt.add(x1[0] == 3)
opt.add(y1[0] == 3)
opt.add(b1[0] == 6)

opt.add(x2[0] == 2)
opt.add(y2[0] == 2)
opt.add(b2[0] == 4)

opt.add(xc[0] == 1)
opt.add(yc[0] == 1)

for t in range(T):
    opt.add(x0[t] >= 0, x0[t] < rows)
    opt.add(y0[t] >= 0, y0[t] < cols)
    opt.add(x1[t] >= 0, x1[t] < rows)
    opt.add(y1[t] >= 0, y1[t] < cols)
    opt.add(x2[t] >= 0, x2[t] < rows)
    opt.add(y2[t] >= 0, y2[t] < cols)
    opt.add(xc[t] >= 0, xc[t] < rows)
    opt.add(yc[t] >= 0, yc[t] < cols)

for t in range(T-1):
    opt.add(Abs(x0[t+1]-x0[t]) + Abs(y0[t+1]-y0[t]) <= 1)
    opt.add(Abs(x1[t+1]-x1[t]) + Abs(y1[t+1]-y1[t]) <= 1)
    opt.add(Abs(x2[t+1]-x2[t]) + Abs(y2[t+1]-y2[t]) <= 1)
    opt.add(Abs(xc[t+1]-xc[t]) + Abs(yc[t+1]-yc[t]) <= 1)

cost = [1 + random.uniform(0,0.5) for _ in range(T)]

for t in range(T-1):
    opt.add(b0[t+1] == If(charge0[t], b0[t] + 5, b0[t] - cost[t]))
    opt.add(b1[t+1] == If(charge1[t], b1[t] + 5, b1[t] - cost[t]))
    opt.add(b2[t+1] == If(charge2[t], b2[t] + 5, b2[t] - cost[t]))

for t in range(T):
    opt.add(Implies(charge0[t], And(xc[t] == x0[t], yc[t] == y0[t])))
    opt.add(Implies(charge1[t], And(xc[t] == x1[t], yc[t] == y1[t])))
    opt.add(Implies(charge2[t], And(xc[t] == x2[t], yc[t] == y2[t])))

for t in range(T):
    opt.add(Sum([If(charge0[t],1,0),If(charge1[t],1,0),If(charge2[t],1,0)]) <= 1)

for t in range(T):
    opt.add(wait0[t] == If(And(b0[t] <= 0, Not(charge0[t])),1,0))
    opt.add(wait1[t] == If(And(b1[t] <= 0, Not(charge1[t])),1,0))
    opt.add(wait2[t] == If(And(b2[t] <= 0, Not(charge2[t])),1,0))

total_wait = Sum([Sum(wait0),Sum(wait1),Sum(wait2)])
opt.minimize(total_wait)

if opt.check() == sat:
    m = opt.model()
    print('Total wait:', m.evaluate(total_wait))

    print('\nWorker',0)
    for t in range(T):
        print(t, m.evaluate(x0[t]), m.evaluate(y0[t]), m.evaluate(b0[t]))
    print('\nWorker',1)
    for t in range(T):
        print(t, m.evaluate(x1[t]), m.evaluate(y1[t]), m.evaluate(b1[t]))
    print('\nWorker',2)
    for t in range(T):
        print(t, m.evaluate(x2[t]), m.evaluate(y2[t]), m.evaluate(b2[t]))
