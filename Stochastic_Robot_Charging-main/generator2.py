# generator_same_logic.py
from z3 import *

workers = int(input("Number of workers: "))
chargers = int(input("Number of chargers: "))

rows = int(input("Grid rows: "))
cols = int(input("Grid cols: "))
T = int(input("Time horizon: "))

file = open("generated_model.py","w")

file.write("from z3 import *\n\n")

file.write(f"workers={workers}\n")
file.write(f"chargers={chargers}\n")
file.write(f"rows={rows}\n")
file.write(f"cols={cols}\n")
file.write(f"T={T}\n\n")

file.write("opt = Optimize()\n\n")

# ---------------- WORKER VARIABLES ----------------

for w in range(workers):

    file.write(f"x{w}=[Int('x{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"y{w}=[Int('y{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"b{w}=[Real('b{w}_'+str(t)) for t in range(T)]\n")
    file.write(f"wait{w}=[Int('wait{w}_'+str(t)) for t in range(T)]\n\n")

# ---------------- CHARGER VARIABLES ----------------

for c in range(chargers):

    file.write(f"xc{c}=[Int('xc{c}_'+str(t)) for t in range(T)]\n")
    file.write(f"yc{c}=[Int('yc{c}_'+str(t)) for t in range(T)]\n\n")

# ---------------- ASSIGNMENT VARIABLES ----------------

for w in range(workers):
    for c in range(chargers):

        file.write(
        f"assign_{w}_{c}=[Bool('assign_{w}_{c}_'+str(t)) for t in range(T)]\n"
        )

file.write("\n")

# ---------------- INITIAL CONDITIONS ----------------

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

# ---------------- GRID BOUNDS ----------------

file.write("for t in range(T):\n")

for w in range(workers):

    file.write(f" opt.add(x{w}[t]>=0,x{w}[t]<rows)\n")
    file.write(f" opt.add(y{w}[t]>=0,y{w}[t]<cols)\n")

for c in range(chargers):

    file.write(f" opt.add(xc{c}[t]>=0,xc{c}[t]<rows)\n")
    file.write(f" opt.add(yc{c}[t]>=0,yc{c}[t]<cols)\n")

file.write("\n")

# ---------------- MOTION ----------------

file.write("for t in range(T-1):\n")

for w in range(workers):

    file.write(
    f" opt.add(Abs(x{w}[t+1]-x{w}[t])+Abs(y{w}[t+1]-y{w}[t])<=1)\n"
    )

for c in range(chargers):

    file.write(
    f" opt.add(Abs(xc{c}[t+1]-xc{c}[t])+Abs(yc{c}[t+1]-yc{c}[t])<=1)\n"
    )

file.write("\n")

# ---------------- ROBOT STOPS IF DEAD ----------------

file.write("for t in range(T-1):\n")

for w in range(workers):

    file.write(
    f" opt.add(If(b{w}[t]<=0, And(x{w}[t+1]==x{w}[t], y{w}[t+1]==y{w}[t]), True))\n"
    )

file.write("\n")

# ---------------- CHARGING LOCATION ----------------

file.write("for t in range(T):\n")

for w in range(workers):
    for c in range(chargers):

        file.write(
        f" opt.add(Implies(assign_{w}_{c}[t],"
        f"And(xc{c}[t]==x{w}[t], yc{c}[t]==y{w}[t])))\n"
        )

file.write("\n")

# ---------------- ONE CHARGER PER WORKER ----------------

file.write("for t in range(T):\n")

for w in range(workers):

    file.write(
    f" opt.add(Sum([If(assign_{w}_{c}[t],1,0) for c in range(chargers)])<=1)\n"
    )

file.write("\n")

# ---------------- ONE WORKER PER CHARGER ----------------

for c in range(chargers):

    file.write(
    f"for t in range(T): opt.add(Sum([If(assign_{w}_{c}[t],1,0) for w in range(workers)])<=1)\n"
    )

file.write("\n")

# ---------------- REACTIVE CHARGING ----------------

file.write("for t in range(T):\n")

for w in range(workers):
    for c in range(chargers):

        file.write(
        f" opt.add(Implies(assign_{w}_{c}[t], b{w}[t] <= 0))\n"
        )

file.write("\n")

# ---------------- BATTERY UPDATE ----------------

file.write("for t in range(T-1):\n")

for w in range(workers):

    file.write(
    f" opt.add(b{w}[t+1]==If(Or([assign_{w}_{c}[t] for c in range(chargers)]),"
    f" b{w}[t]+5, b{w}[t]-1))\n"
    )

file.write("\n")

# ---------------- WAIT TIME ----------------

file.write("for t in range(T):\n")

for w in range(workers):

    file.write(
    f" opt.add(wait{w}[t]==If(And(b{w}[t]<=0,"
    f"Not(Or([assign_{w}_{c}[t] for c in range(chargers)]))),1,0))\n"
    )

file.write("\n")

# ---------------- OBJECTIVE ----------------

file.write("total_wait = Sum([")

for w in range(workers):

    if w != workers-1:
        file.write(f"Sum(wait{w}),")
    else:
        file.write(f"Sum(wait{w})")

file.write("])\n")

file.write("opt.minimize(total_wait)\n\n")

file.write("if opt.check()==sat:\n")
file.write(" m=opt.model()\n")
file.write(" print('Total wait:',m.evaluate(total_wait))\n")
file.write("else:\n")
file.write(" print('UNSAT')\n")

file.close()

print("Generated model with same logic as base program")