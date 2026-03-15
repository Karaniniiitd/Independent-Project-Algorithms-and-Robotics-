from z3 import *
import random

# ---------------- USER INPUT ----------------

rows = int(input("Enter grid rows: "))
cols = int(input("Enter grid cols: "))
T = int(input("Enter time horizon: "))

if T < 2:
    print("Time horizon must be >= 2")
    exit()

n = int(input("Enter number of worker robots: "))
c = int(input("Enter number of charging robots: "))

# ---------------- INITIAL POSITIONS ----------------

worker_start = []
for i in range(n):
    x = int(input(f"Worker {i} start x: "))
    y = int(input(f"Worker {i} start y: "))
    worker_start.append((x,y))

charger_start = []
for j in range(c):
    x = int(input(f"Charger {j} start x: "))
    y = int(input(f"Charger {j} start y: "))
    charger_start.append((x,y))

# ---------------- BATTERY ----------------

b_init = []
for i in range(n):
    b_init.append(int(input(f"Worker {i} initial battery: ")))

CHARGE_RATE = 5

# ---------------- STOCHASTIC DISCHARGE ----------------

cost = [
    [1 + random.uniform(0,0.5) for _ in range(T)]
    for _ in range(n)
]

# ---------------- SOLVER ----------------

opt = Optimize()

# ---------------- VARIABLES ----------------

# worker positions
x = [[Int(f"x_{i}_{t}") for t in range(T)] for i in range(n)]
y = [[Int(f"y_{i}_{t}") for t in range(T)] for i in range(n)]

# charger positions
xc = [[Int(f"xc_{j}_{t}") for t in range(T)] for j in range(c)]
yc = [[Int(f"yc_{j}_{t}") for t in range(T)] for j in range(c)]

# battery
b = [[Real(f"b_{i}_{t}") for t in range(T)] for i in range(n)]

# charging decision
charge = [[[Bool(f"charge_{j}_{i}_{t}") for t in range(T)]
            for i in range(n)]
            for j in range(c)]

# waiting
wait = [[Int(f"wait_{i}_{t}") for t in range(T)] for i in range(n)]

# ---------------- INITIAL CONDITIONS ----------------

for i in range(n):

    opt.add(x[i][0] == worker_start[i][0])
    opt.add(y[i][0] == worker_start[i][1])

    opt.add(b[i][0] == b_init[i])

for j in range(c):

    opt.add(xc[j][0] == charger_start[j][0])
    opt.add(yc[j][0] == charger_start[j][1])

# ---------------- GRID BOUNDS ----------------

for i in range(n):
    for t in range(T):

        opt.add(x[i][t] >= 0, x[i][t] < rows)
        opt.add(y[i][t] >= 0, y[i][t] < cols)

for j in range(c):
    for t in range(T):

        opt.add(xc[j][t] >= 0, xc[j][t] < rows)
        opt.add(yc[j][t] >= 0, yc[j][t] < cols)

# ---------------- MOTION ----------------

for i in range(n):
    for t in range(T-1):

        opt.add(
            Abs(x[i][t+1]-x[i][t]) +
            Abs(y[i][t+1]-y[i][t]) <= 1
        )

for j in range(c):
    for t in range(T-1):

        opt.add(
            Abs(xc[j][t+1]-xc[j][t]) +
            Abs(yc[j][t+1]-yc[j][t]) <= 1
        )

# ---------------- STOP IF BATTERY DEAD ----------------

for i in range(n):
    for t in range(T-1):

        opt.add(
            If(b[i][t] <= 0,
               And(x[i][t+1] == x[i][t],
                   y[i][t+1] == y[i][t]),
               True)
        )

# ---------------- CHARGING LOCATION ----------------

for j in range(c):
    for i in range(n):
        for t in range(T):

            opt.add(
                Implies(
                    charge[j][i][t],
                    And(
                        xc[j][t] == x[i][t],
                        yc[j][t] == y[i][t]
                    )
                )
            )

# ---------------- ONE CHARGER PER WORKER ----------------

for i in range(n):
    for t in range(T):

        opt.add(
            Sum([
                If(charge[j][i][t],1,0)
                for j in range(c)
            ]) <= 1
        )

# ---------------- ONE WORKER PER CHARGER ----------------

for j in range(c):
    for t in range(T):

        opt.add(
            Sum([
                If(charge[j][i][t],1,0)
                for i in range(n)
            ]) <= 1
        )

# ---------------- BATTERY UPDATE ----------------

for i in range(n):
    for t in range(T-1):

        charging_now = Or([charge[j][i][t] for j in range(c)])

        opt.add(
            b[i][t+1] ==
            If(charging_now,
               b[i][t] + CHARGE_RATE,
               b[i][t] - cost[i][t])
        )

# ---------------- WAITING TIME ----------------

for i in range(n):
    for t in range(T):

        charging_now = Or([charge[j][i][t] for j in range(c)])

        opt.add(
            wait[i][t] ==
            If(And(b[i][t] <= 0, Not(charging_now)), 1, 0)
        )

# ---------------- OBJECTIVE ----------------

total_wait = Sum([
    wait[i][t]
    for i in range(n)
    for t in range(T)
])

opt.minimize(total_wait)

# ---------------- SOLVE ----------------

print("\nSolving...")

if opt.check() == sat:

    m = opt.model()

    print("\nMinimum total wait time:",
          m.evaluate(total_wait))

else:
    print("UNSAT")