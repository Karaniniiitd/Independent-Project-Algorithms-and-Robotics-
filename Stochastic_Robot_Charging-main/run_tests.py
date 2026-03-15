import subprocess
import os

base_dir = os.path.dirname(__file__)

solver_file = os.path.join(base_dir, "Dynamic2.py")
test_file = os.path.join(base_dir, "testCases.txt")

with open(test_file, "r") as f:
    data = f.read()

process = subprocess.Popen(
    ["python", solver_file],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

output, error = process.communicate(input=data)

print("----- Solver Output -----")
print(output)

if error:
    print("Errors:")
    print(error)