import subprocess

for compiler in ["gcc", "clang"]:

    print(f"\nTesting with {compiler.upper()}...")

    executable = f"results/timeout_{compiler}.exe"

    subprocess.run([
        compiler,
        "-std=c11",
        "inputs/infinite_loop.c",
        "-o",
        executable
    ], check=True)

    try:
        subprocess.run(
            [executable],
            timeout=5
        )

        print("Execution completed.")

    except subprocess.TimeoutExpired:
        print(f"{compiler.upper()}: Infinite loop detected (Timeout)!")