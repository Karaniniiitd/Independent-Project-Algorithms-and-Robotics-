from z3 import *
import random

# =============================
# USER INPUT
# =============================

workers = int(input("Number of workers: "))
chargers = int(input("Number of chargers: "))

rows = int(input("Enter rows: "))
cols = int(input("Enter cols: "))
T = int(input("Enter time horizon: "))

if T < 2:
    print("Time horizon must be >= 2")
    exit()

# =============================
# START POSITIONS
# =============================

worker_start = []
for w in range(workers):
    x = int(input(f"Worker{w} start x: "))
    y = int(input(f"Worker{w} start y: "))
    worker_start.append((x, y))

charger_start = []
for c in range(chargers):
    x = int(input(f"Charger{c} start x: "))
    y = int(input(f"Charger{c} start y: "))
    charger_start.append((x, y))

# =============================
# BATTERY INITIAL
# =============================

battery_init = []
for w in range(workers):
    b = int(input(f"Worker{w} battery: "))
    battery_init.append(b)

# =============================
# STOCHASTIC BATTERY DISCHARGE
# =============================

cost = [[1 + random.uniform(0,0.5) for _ in range(T)] for _ in range(workers)]

# =============================
# SOLVER
# =============================

opt = Optimize()

# =============================
# VARIABLES
# =============================

x = [[Int(f"x_{w}_{t}") for t in range(T)] for w in range(workers)]
y = [[Int(f"y_{w}_{t}") for t in range(T)] for w in range(workers)]

xc = [[Int(f"xc_{c}_{t}") for t in range(T)] for c in range(chargers)]
yc = [[Int(f"yc_{c}_{t}") for t in range(T)] for c in range(chargers)]

b = [[Real(f"b_{w}_{t}") for t in range(T)] for w in range(workers)]

assign = [[[Bool(f"assign_{w}_{c}_{t}") for t in range(T)]
           for c in range(chargers)]
           for w in range(workers)]

wait = [[Int(f"wait_{w}_{t}") for t in range(T)] for w in range(workers)]

# =============================
# INITIAL CONDITIONS
# =============================

for w in range(workers):
    opt.add(x[w][0] == worker_start[w][0])
    opt.add(y[w][0] == worker_start[w][1])
    opt.add(b[w][0] == battery_init[w])

for c in range(chargers):
    opt.add(xc[c][0] == charger_start[c][0])
    opt.add(yc[c][0] == charger_start[c][1])

# =============================
# GRID BOUNDS
# =============================

for t in range(T):

    for w in range(workers):
        opt.add(x[w][t] >= 0, x[w][t] < rows)
        opt.add(y[w][t] >= 0, y[w][t] < cols)

    for c in range(chargers):
        opt.add(xc[c][t] >= 0, xc[c][t] < rows)
        opt.add(yc[c][t] >= 0, yc[c][t] < cols)

# =============================
# MOVEMENT CONSTRAINTS
# =============================

for t in range(T-1):

    for w in range(workers):
        opt.add(
            Abs(x[w][t+1] - x[w][t]) +
            Abs(y[w][t+1] - y[w][t]) <= 1
        )

    for c in range(chargers):
        opt.add(
            Abs(xc[c][t+1] - xc[c][t]) +
            Abs(yc[c][t+1] - yc[c][t]) <= 1
        )

# =============================
# ROBOT STOPS IF BATTERY DEAD
# =============================

for t in range(T-1):
    for w in range(workers):

        opt.add(
            If(
                b[w][t] <= 0,
                And(x[w][t+1] == x[w][t],
                    y[w][t+1] == y[w][t]),
                True
            )
        )

# =============================
# CHARGER ASSIGNMENT RULES
# =============================

for t in range(T):

    # each charger serves ≤1 worker
    for c in range(chargers):
        opt.add(
            Sum([If(assign[w][c][t],1,0)
                 for w in range(workers)]) <= 1
        )

    # each worker gets ≤1 charger
    for w in range(workers):
        opt.add(
            Sum([If(assign[w][c][t],1,0)
                 for c in range(chargers)]) <= 1
        )

# =============================
# CHARGING LOCATION
# =============================

for t in range(T):
    for w in range(workers):
        for c in range(chargers):

            opt.add(
                Implies(
                    assign[w][c][t],
                    And(xc[c][t] == x[w][t],
                        yc[c][t] == y[w][t])
                )
            )

# =============================
# REACTIVE CHARGING
# =============================

for t in range(T):
    for w in range(workers):
        for c in range(chargers):

            opt.add(
                Implies(assign[w][c][t], b[w][t] <= 0)
            )

# =============================
# BATTERY UPDATE
# =============================

for t in range(T-1):
    for w in range(workers):

        charge_gain = Sum([
            If(assign[w][c][t], 5, 0)
            for c in range(chargers)
        ])

        opt.add(
            b[w][t+1] ==
            b[w][t] - cost[w][t] + charge_gain
        )

# =============================
# WAITING TIME
# =============================

for t in range(T):
    for w in range(workers):

        charging_now = Or([assign[w][c][t] for c in range(chargers)])

        opt.add(
            wait[w][t] ==
            If(And(b[w][t] <= 0, Not(charging_now)),1,0)
        )

# =============================
# OBJECTIVE
# =============================

total_wait = Sum([Sum(wait[w]) for w in range(workers)])

opt.minimize(total_wait)

# =============================
# SOLVE
# =============================

if opt.check() == sat:

    m = opt.model()

    print("\nTotal wait:", m.evaluate(total_wait))

else:

    print("UNSAT")