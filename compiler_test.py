
import subprocess
import csv
import os

def test_compilers(source_file, input_file, mutation_name):

    compilers = ["gcc", "clang"]
    results = {}

    for compiler in compilers:

        print(f"\nTesting with {compiler.upper()}...")

        executable = f"results/{compiler}_program.exe"

        command = [
            compiler, "-std=c11", "-Wall", "-Wextra",
            source_file, "-o", executable
        ]

        try:
            compilation = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if compilation.returncode != 0:
                print(f"{compiler.upper()}: Compilation failed")
                results[compiler] = {
                    "status": "Failed",
                    "exit_code": "N/A"
                }
                continue

            print(f"{compiler.upper()}: Compilation successful")

            execution = subprocess.run(
                [executable],
                capture_output=True,
                text=True
            )

            results[compiler] = {
                "status": "Success",
                "exit_code": execution.returncode
            }

            print(f"Execution exit code: {execution.returncode}")

        except FileNotFoundError:
            print(f"{compiler.upper()} was not found.")
            results[compiler] = {
                "status": "Compiler not found",
                "exit_code": "N/A"
            }

    # Compare results
    gcc_result = results["gcc"]
    clang_result = results["clang"]

    if (gcc_result["status"] == "Success"
            and clang_result["status"] == "Success"):

        if gcc_result["exit_code"] == clang_result["exit_code"]:
            comparison = "Match"
        else:
            comparison = "Difference detected"
    else:
        comparison = "Comparison incomplete"

    print("\n--- COMPILER COMPARISON ---")
    print(comparison)

    # Save one row per test
    report_file = "results/comparison_report.csv"
    file_exists = os.path.isfile(report_file)

    with open(report_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Input File",
                "Mutation",
                "GCC Status",
                "GCC Exit Code",
                "Clang Status",
                "Clang Exit Code",
                "Comparison"
            ])

        writer.writerow([
            input_file,
            mutation_name,
            gcc_result["status"],
            gcc_result["exit_code"],
            clang_result["status"],
            clang_result["exit_code"],
            comparison
        ])

    print(f"Results saved to {report_file}")
