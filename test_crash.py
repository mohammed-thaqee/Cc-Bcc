import subprocess
from compiler_test import is_abnormal_termination

for compiler in ["gcc", "clang"]:

    print(f"\nTesting with {compiler.upper()}...")

    executable = f"results/crash_{compiler}.exe"

    subprocess.run([
        compiler,
        "-std=c11",
        "inputs/crash.c",
        "-o",
        executable
    ], check=True)

    try:
        execution = subprocess.run(
            [executable],
            capture_output=True,
            text=True,
            timeout=5
        )

        print("Exit code:", execution.returncode)

        if is_abnormal_termination(execution.returncode):
            print("Crash detected!")
        else:
            print("No crash detected.")

    except subprocess.TimeoutExpired:
        print("Execution timed out!")