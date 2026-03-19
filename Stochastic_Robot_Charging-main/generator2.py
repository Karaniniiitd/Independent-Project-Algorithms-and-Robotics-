# generator_same_logic_random_fixed.py

from z3 import *
import random

workers = int(input("Number of workers: "))
chargers = int(input("Number of chargers: "))

rows = int(input("Grid rows: "))
cols = int(input("Grid cols: "))
T = int(input("Time horizon: "))

random.seed(0)

file = open("generated_model.py","w")

file.write("from z3 import *\n\n")

file.write(f"workers={workers}\n")
file.write(f"chargers={chargers}\n")
file.write(f"rows={rows}\n")
file.write(f"cols={cols}\n")
file.write(f"T={T}\n\n")

file.write("opt = Optimize()\n\n")

# Random discharge matrix
cost = [[1 + random.uniform(0,0.5) for _ in range(T)] for _ in range(workers)]
file.write("cost = " + str(cost) + "\n\n")

# Worker variables
for w in range(workers):

    file.write(f"x{w}=[Int('x{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"y{w}=[Int('y{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"b{w}=[Real('b{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"wait{w}=[Int('wait{w}_'+str(t)) for t in range(T)]\n\n")

# Charger variables
for c in range(chargers):

    file.write(f"xc{c}=[Int('xc{c}_'+str(t)) for t in range(T)]\n")
    file.write(f"yc{c}=[Int('yc{c}_'+str(t)) for t in range(T)]\n\n")

# Assignment variables
for w in range(workers):
    for c in range(chargers):

        file.write(
        f"assign_{w}_{c}=[Bool('assign_{w}_{c}_'+str(t)) for t in range(T)]\n"
        )

file.write("\n")

# Initial conditions
for w in range(workers):

    x=int(input(f"Worker {w} start x: "))
    y=int(input(f"Worker {w} start y: "))
    b=int(input(f"Worker {w} battery: "))

    file.write(f"opt.add(x{w}[0]=={x})\n")
    file.write(f"opt.add(y{w}[0]=={y})\n")
    file.write(f"opt.add(b{w}[0]=={b})\n\n")

for c in range(chargers):

    x=int(input(f"Charger {c} start x: "))
    y=int(input(f"Charger {c} start y: "))

    file.write(f"opt.add(xc{c}[0]=={x})\n")
    file.write(f"opt.add(yc{c}[0]=={y})\n\n")

# Grid bounds
file.write("for t in range(T):\n")

for w in range(workers):

    file.write(f" opt.add(x{w}[t]>=0,x{w}[t]<rows)\n")
    file.write(f" opt.add(y{w}[t]>=0,y{w}[t]<cols)\n")

for c in range(chargers):

    file.write(f" opt.add(xc{c}[t]>=0,xc{c}[t]<rows)\n")
    file.write(f" opt.add(yc{c}[t]>=0,yc{c}[t]<cols)\n")

# Movement
file.write("\nfor t in range(T-1):\n")

for w in range(workers):

    file.write(
    f" opt.add(Abs(x{w}[t+1]-x{w}[t])+Abs(y{w}[t+1]-y{w}[t])<=1)\n"
    )

for c in range(chargers):

    file.write(
    f" opt.add(Abs(xc{c}[t+1]-xc{c}[t])+Abs(yc{c}[t+1]-yc{c}[t])<=1)\n"
    )

# Stop if battery dead
file.write("\nfor t in range(T-1):\n")

for w in range(workers):

    file.write(
    f" opt.add(If(b{w}[t]<=0, And(x{w}[t+1]==x{w}[t], y{w}[t+1]==y{w}[t]), True))\n"
    )

# Charging location
file.write("\nfor t in range(T):\n")

for w in range(workers):
    for c in range(chargers):

        file.write(
        f" opt.add(Implies(assign_{w}_{c}[t],"
        f"And(xc{c}[t]==x{w}[t], yc{c}[t]==y{w}[t])))\n"
        )

# Charger constraints
file.write("\nfor t in range(T):\n")

for w in range(workers):

    worker_assign_terms = ",".join([f"If(assign_{w}_{ch}[t],1,0)" for ch in range(chargers)])

    file.write(
    f" opt.add(Sum([{worker_assign_terms}])<=1)\n"
    )

for c in range(chargers):

    charger_assign_terms = ",".join([f"If(assign_{wk}_{c}[t],1,0)" for wk in range(workers)])

    file.write(
    f" opt.add(Sum([{charger_assign_terms}])<=1)\n"
    )

# Reactive charging
file.write("\nfor t in range(T):\n")

for w in range(workers):
    for c in range(chargers):

        file.write(
        f" opt.add(Implies(assign_{w}_{c}[t], b{w}[t] <= 0))\n"
        )

# Battery update
file.write("\nfor t in range(T-1):\n")

for w in range(workers):

    charge_terms = ",".join([f"assign_{w}_{c}[t]" for c in range(chargers)])

    file.write(
    f" opt.add(b{w}[t+1]==If(Or({charge_terms}), b{w}[t]+5, b{w}[t]-cost[{w}][t]))\n"
    )

# Wait
file.write("\nfor t in range(T):\n")

for w in range(workers):

    charge_terms = ",".join([f"assign_{w}_{c}[t]" for c in range(chargers)])

    file.write(
    f" opt.add(wait{w}[t]==If(And(b{w}[t]<=0,Not(Or({charge_terms}))),1,0))\n"
    )

# Objective
file.write("\ntotal_wait = Sum([")

for w in range(workers):

    if w != workers-1:
        file.write(f"Sum(wait{w}),")
    else:
        file.write(f"Sum(wait{w})")

file.write("])\n")

file.write("opt.minimize(total_wait)\n")

file.write("""
if opt.check()==sat:
 m=opt.model()
 print("Total wait:",m.evaluate(total_wait))
else:
 print("UNSAT")
""")

file.close()

print("Generated model successfully")