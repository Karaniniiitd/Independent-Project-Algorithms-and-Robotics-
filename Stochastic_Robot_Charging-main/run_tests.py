import os
import re
import subprocess
import sys


BASE_DIR = os.path.dirname(__file__)
TEST_FILE = os.path.join(BASE_DIR, "testCases.txt")
DYNAMIC3_FILE = os.path.join(BASE_DIR, "Dynamic3.py")
GENERATOR2_FILE = os.path.join(BASE_DIR, "generator2.py")
GENERATED_MODEL_FILE = os.path.join(BASE_DIR, "generated_model.py")


def parse_case_block(block: str, case_index: int):
    values = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            values.append(int(line))
        except ValueError as exc:
            raise ValueError(f"Case {case_index}: non-integer input '{line}'") from exc

    if len(values) < 5:
        raise ValueError(f"Case {case_index}: expected at least 5 numbers, got {len(values)}")

    n = values[0]
    c = values[1]
    expected = 5 + (3 * n) + (2 * c)
    if len(values) != expected:
        raise ValueError(
            f"Case {case_index}: expected {expected} numbers for n={n}, c={c}, got {len(values)}"
        )
    return values


def load_test_cases(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    blocks = [b for b in re.split(r"\n\s*\n+", content) if b.strip()]
    cases = []
    for idx, block in enumerate(blocks, 1):
        cases.append(parse_case_block(block, idx))
    return cases


def run_python(file_path: str, stdin_data: str = ""):
    return subprocess.run(
        [sys.executable, file_path],
        input=stdin_data,
        text=True,
        capture_output=True,
        cwd=BASE_DIR,
        timeout=60,
    )


def extract_wait(output: str, label: str):
    match = re.search(rf"{re.escape(label)}\s*(-?\d+)", output)
    return int(match.group(1)) if match else None


def main():
    try:
        cases = load_test_cases(TEST_FILE)
    except Exception as exc:
        print(f"Failed to read test cases: {exc}")
        return

    if not cases:
        print("No test cases found in testCases.txt")
        return

    print(f"Loaded {len(cases)} test case(s) from testCases.txt")
    print()

    passed = 0

    for idx, case in enumerate(cases, 1):
        case_input = "\n".join(str(x) for x in case) + "\n"

        dynamic3 = run_python(DYNAMIC3_FILE, case_input)
        generator2 = run_python(GENERATOR2_FILE, case_input)

        generated_model = None
        if generator2.returncode == 0 and os.path.exists(GENERATED_MODEL_FILE):
            generated_model = run_python(GENERATED_MODEL_FILE)

        min_wait = extract_wait(dynamic3.stdout, "Minimum wait:")
        total_wait = extract_wait(generated_model.stdout if generated_model else "", "Total wait:")

        has_runtime_error = any([
            dynamic3.returncode != 0,
            generator2.returncode != 0,
            generated_model is None,
            (generated_model is not None and generated_model.returncode != 0),
        ])

        print(f"Case {idx}: n={case[0]}, c={case[1]}")

        if has_runtime_error:
            print("  Status: ERROR")
            if dynamic3.returncode != 0:
                print("  Dynamic3 stderr:")
                print(dynamic3.stderr.strip() or "<no stderr>")
            if generator2.returncode != 0:
                print("  generator2 stderr:")
                print(generator2.stderr.strip() or "<no stderr>")
            if generated_model is None:
                print("  generated_model.py was not created")
            elif generated_model.returncode != 0:
                print("  generated_model stderr:")
                print(generated_model.stderr.strip() or "<no stderr>")
            print()
            continue

        print(f"  Dynamic3 minimum wait: {min_wait}")
        print(f"  generated_model total wait: {total_wait}")

        if min_wait is None or total_wait is None:
            print("  Status: FAIL (could not parse wait value)")
        elif min_wait == total_wait:
            print("  Status: PASS")
            passed += 1
        else:
            print("  Status: FAIL (wait values differ)")
        print()

    print(f"Summary: {passed}/{len(cases)} case(s) passed")


if __name__ == "__main__":
    main()