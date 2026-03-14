# generator.py
# This program generates a Z3 constraint model automatically

num_robots = int(input("Enter number of robots: "))
time_steps = int(input("Enter number of time steps: "))

# open file that will contain solver code
file = open("generated_model.py", "w")

# write imports
file.write("from z3 import *\n\n")

file.write("solver = Solver()\n\n")

# =========================
# VARIABLE GENERATION
# =========================

file.write("# Robot position variables\n")

for i in range(num_robots):
    for t in range(time_steps):
        file.write(f"x_{i}_{t} = Int('x_{i}_{t}')\n")
        file.write(f"y_{i}_{t} = Int('y_{i}_{t}')\n")

file.write("\n")

# =========================
# INITIAL POSITION INPUT
# =========================

file.write("# Initial position constraints\n")

for i in range(num_robots):
    x = int(input(f"Initial X position for robot {i}: "))
    y = int(input(f"Initial Y position for robot {i}: "))

    file.write(f"solver.add(x_{i}_0 == {x})\n")
    file.write(f"solver.add(y_{i}_0 == {y})\n")

file.write("\n")

# =========================
# GRID BOUNDARY CONSTRAINT
# =========================

grid_size = int(input("Enter grid size: "))

file.write("# Grid boundary constraints\n")

for i in range(num_robots):
    for t in range(time_steps):

        file.write(f"solver.add(x_{i}_{t} >= 0)\n")
        file.write(f"solver.add(x_{i}_{t} <= {grid_size})\n")

        file.write(f"solver.add(y_{i}_{t} >= 0)\n")
        file.write(f"solver.add(y_{i}_{t} <= {grid_size})\n")

file.write("\n")

# =========================
# MOVEMENT CONSTRAINT
# =========================

file.write("# Movement constraints (Manhattan distance <= 1)\n")

for i in range(num_robots):
    for t in range(time_steps - 1):

        file.write(
            f"solver.add(Abs(x_{i}_{t+1} - x_{i}_{t}) + Abs(y_{i}_{t+1} - y_{i}_{t}) <= 1)\n"
        )

file.write("\n")

# =========================
# SOLVER OUTPUT
# =========================

file.write("result = solver.check()\n")
file.write("print('Solver result:', result)\n")

file.write("if result == sat:\n")
file.write("    model = solver.model()\n")
file.write("    print('\\nModel:')\n")

for i in range(num_robots):
    for t in range(time_steps):
        file.write(f"    print('Robot {i} at time {t}:', model[x_{i}_{t}], model[y_{i}_{t}])\n")

file.close()

print("\n✅ Solver model generated successfully!")
print("Run 'python generated_model.py' to execute it.")