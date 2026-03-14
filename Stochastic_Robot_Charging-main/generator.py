# generator.py
# Generates a full worker-charger Z3 model automatically

num_workers = int(input("Number of workers: "))
rows = int(input("Grid rows: "))
cols = int(input("Grid cols: "))
T = int(input("Time horizon: "))

file = open("generated_model.py","w")

file.write("from z3 import *\n")
file.write("import random\n\n")

file.write(f"rows = {rows}\n")
file.write(f"cols = {cols}\n")
file.write(f"T = {T}\n\n")

file.write("opt = Optimize()\n\n")

# WORKER VARIABLES
for i in range(num_workers):

    file.write(f"x{i} = [Int('x{i}_'+str(t)) for t in range(T)]\n")
    file.write(f"y{i} = [Int('y{i}_'+str(t)) for t in range(T)]\n")
    file.write(f"b{i} = [Real('b{i}_'+str(t)) for t in range(T)]\n")
    file.write(f"charge{i} = [Bool('charge{i}_'+str(t)) for t in range(T)]\n")
    file.write(f"wait{i} = [Int('wait{i}_'+str(t)) for t in range(T)]\n\n")

# CHARGER VARIABLES
file.write("xc = [Int('xc_'+str(t)) for t in range(T)]\n")
file.write("yc = [Int('yc_'+str(t)) for t in range(T)]\n\n")

# INITIAL CONDITIONS
for i in range(num_workers):

    x = int(input(f"Worker {i} start x: "))
    y = int(input(f"Worker {i} start y: "))
    b = int(input(f"Worker {i} battery: "))

    file.write(f"opt.add(x{i}[0] == {x})\n")
    file.write(f"opt.add(y{i}[0] == {y})\n")
    file.write(f"opt.add(b{i}[0] == {b})\n\n")

cx = int(input("Charger start x: "))
cy = int(input("Charger start y: "))

file.write(f"opt.add(xc[0] == {cx})\n")
file.write(f"opt.add(yc[0] == {cy})\n\n")

# GRID BOUNDS
file.write("for t in range(T):\n")

for i in range(num_workers):

    file.write(f"    opt.add(x{i}[t] >= 0, x{i}[t] < rows)\n")
    file.write(f"    opt.add(y{i}[t] >= 0, y{i}[t] < cols)\n")

file.write("    opt.add(xc[t] >= 0, xc[t] < rows)\n")
file.write("    opt.add(yc[t] >= 0, yc[t] < cols)\n\n")

# MOVEMENT CONSTRAINTS
file.write("for t in range(T-1):\n")

for i in range(num_workers):

    file.write(f"    opt.add(Abs(x{i}[t+1]-x{i}[t]) + Abs(y{i}[t+1]-y{i}[t]) <= 1)\n")

file.write("    opt.add(Abs(xc[t+1]-xc[t]) + Abs(yc[t+1]-yc[t]) <= 1)\n\n")

# BATTERY UPDATE
file.write("cost = [1 + random.uniform(0,0.5) for _ in range(T)]\n\n")

file.write("for t in range(T-1):\n")

for i in range(num_workers):

    file.write(
        f"    opt.add(b{i}[t+1] == If(charge{i}[t], b{i}[t] + 5, b{i}[t] - cost[t]))\n"
    )

file.write("\n")

# CHARGING LOCATION
file.write("for t in range(T):\n")

for i in range(num_workers):

    file.write(
        f"    opt.add(Implies(charge{i}[t], And(xc[t] == x{i}[t], yc[t] == y{i}[t])))\n"
    )

file.write("\n")

# ONLY ONE ROBOT CHARGED
file.write("for t in range(T):\n")
file.write("    opt.add(Sum([")

for i in range(num_workers):

    if i != num_workers-1:
        file.write(f"If(charge{i}[t],1,0),")
    else:
        file.write(f"If(charge{i}[t],1,0)")

file.write("]) <= 1)\n\n")

# WAITING TIME
file.write("for t in range(T):\n")

for i in range(num_workers):

    file.write(
        f"    opt.add(wait{i}[t] == If(And(b{i}[t] <= 0, Not(charge{i}[t])),1,0))\n"
    )

file.write("\n")

# OBJECTIVE
file.write("total_wait = Sum([")

for i in range(num_workers):

    if i != num_workers-1:
        file.write(f"Sum(wait{i}),")
    else:
        file.write(f"Sum(wait{i})")

file.write("])\n")

file.write("opt.minimize(total_wait)\n\n")

# SOLVE
file.write("if opt.check() == sat:\n")
file.write("    m = opt.model()\n")
file.write("    print('Total wait:', m.evaluate(total_wait))\n\n")

for i in range(num_workers):

    file.write("    print('\\nWorker',"+str(i)+")\n")
    file.write("    for t in range(T):\n")
    file.write(f"        print(t, m.evaluate(x{i}[t]), m.evaluate(y{i}[t]), m.evaluate(b{i}[t]))\n")

file.close()

print("Model generated successfully -> generated_model.py")