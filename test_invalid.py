
import subprocess

source_file = "inputs/invalid.c"

for compiler in ["gcc", "clang"]:

    print(f"\nTesting with {compiler.upper()}...")

    command = [
        compiler,
        "-std=c11",
        source_file,
        "-o",
        f"results/invalid_{compiler}.exe"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"{compiler.upper()}: Compilation failure detected!")
        print(result.stderr)
    else:
        print(f"{compiler.upper()}: Unexpected compilation success!")
