from z3 import *
import random

rows = int(input("Enter grid rows: "))
cols = int(input("Enter grid cols: "))
T = int(input("Enter time horizon: "))

n = int(input("Enter number of workers: "))
c = int(input("Enter number of chargers: "))

random.seed(0)

worker_start=[]
for i in range(n):
    worker_start.append((int(input(f"Worker {i} start x: ")),
                         int(input(f"Worker {i} start y: "))))

charger_start=[]
for j in range(c):
    charger_start.append((int(input(f"Charger {j} start x: ")),
                          int(input(f"Charger {j} start y: "))))

b_init=[]
for i in range(n):
    b_init.append(int(input(f"Worker {i} battery: ")))

cost=[[1+random.uniform(0,0.5) for _ in range(T)] for _ in range(n)]

opt=Optimize()

x=[[Int(f"x_{i}_{t}") for t in range(T)] for i in range(n)]
y=[[Int(f"y_{i}_{t}") for t in range(T)] for i in range(n)]

xc=[[Int(f"xc_{j}_{t}") for t in range(T)] for j in range(c)]
yc=[[Int(f"yc_{j}_{t}") for t in range(T)] for j in range(c)]

b=[[Real(f"b_{i}_{t}") for t in range(T)] for i in range(n)]

charge=[[[Bool(f"charge_{j}_{i}_{t}") for t in range(T)]
         for i in range(n)]
         for j in range(c)]

wait=[[Int(f"wait_{i}_{t}") for t in range(T)] for i in range(n)]

# initial
for i in range(n):
    opt.add(x[i][0]==worker_start[i][0])
    opt.add(y[i][0]==worker_start[i][1])
    opt.add(b[i][0]==b_init[i])

for j in range(c):
    opt.add(xc[j][0]==charger_start[j][0])
    opt.add(yc[j][0]==charger_start[j][1])

# bounds
for t in range(T):
    for i in range(n):
        opt.add(x[i][t]>=0,x[i][t]<rows)
        opt.add(y[i][t]>=0,y[i][t]<cols)
    for j in range(c):
        opt.add(xc[j][t]>=0,xc[j][t]<rows)
        opt.add(yc[j][t]>=0,yc[j][t]<cols)

# movement
for t in range(T-1):
    for i in range(n):
        opt.add(Abs(x[i][t+1]-x[i][t])+Abs(y[i][t+1]-y[i][t])<=1)
    for j in range(c):
        opt.add(Abs(xc[j][t+1]-xc[j][t])+Abs(yc[j][t+1]-yc[j][t])<=1)

# stop if dead
for t in range(T-1):
    for i in range(n):
        opt.add(If(b[i][t]<=0,
                   And(x[i][t+1]==x[i][t],y[i][t+1]==y[i][t]),
                   True))

# charging location
for t in range(T):
    for j in range(c):
        for i in range(n):
            opt.add(Implies(charge[j][i][t],
                            And(xc[j][t]==x[i][t],
                                yc[j][t]==y[i][t])))

# assignment constraints
for t in range(T):
    for i in range(n):
        opt.add(Sum([If(charge[j][i][t],1,0) for j in range(c)])<=1)
    for j in range(c):
        opt.add(Sum([If(charge[j][i][t],1,0) for i in range(n)])<=1)

# reactive charging
for t in range(T):
    for j in range(c):
        for i in range(n):
            opt.add(Implies(charge[j][i][t],b[i][t]<=0))

# battery update
for t in range(T-1):
    for i in range(n):
        charging_now=Or(*[charge[j][i][t] for j in range(c)])
        opt.add(b[i][t+1]==If(charging_now,b[i][t]+5,b[i][t]-cost[i][t]))

# wait
for t in range(T):
    for i in range(n):
        charging_now=Or(*[charge[j][i][t] for j in range(c)])
        opt.add(wait[i][t]==If(And(b[i][t]<=0,Not(charging_now)),1,0))

total_wait=Sum([wait[i][t] for i in range(n) for t in range(T)])
opt.minimize(total_wait)

if opt.check()==sat:
    m=opt.model()
    print("Minimum wait:",m.evaluate(total_wait))
else:
    print("UNSAT")