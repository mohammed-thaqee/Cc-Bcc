
import subprocess
import csv
import os
import time

def is_abnormal_termination(returncode):

    # POSIX: negative return codes indicate termination by signal
    if returncode < 0:
        return True

    # Windows: common exception/abnormal termination codes
    windows_crash_codes = {
        0xC0000005,  # Access violation
        0xC00000FD,  # Stack overflow
        0xC000001D,  # Illegal instruction
        0x40000015   # Fatal application exit
    }

    return returncode in windows_crash_codes


def test_compilers(source_file, input_file, mutation_name):


    compilers = ["gcc", "clang"]
    optimization_levels = ["-O0", "-O1", "-O2", "-O3"]
    results = {}


    for compiler in compilers:

        for optimization in optimization_levels:

            print(f"\nTesting {compiler.upper()} with {optimization}...")

            executable = f"results/{compiler}_{optimization[1:]}.exe"

            command = [
                compiler,
                "-std=c11",
                "-Wall",
                "-Wextra",
                optimization,
                source_file,
                "-o",
                executable
            ]

            try:
                try:
                    compilation_start = time.perf_counter()

                    compilation = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    compilation_time = time.perf_counter() - compilation_start

                    print(f"Compilation time: {compilation_time:.6f} seconds")

                except subprocess.TimeoutExpired:
                    compilation_time = 10.0
                    
                    print(f"{compiler.upper()}: Compilation timed out!")

                    results[(compiler, optimization)] = {
                        "status": "Compiler Timeout",
                        "stdout": "",
                        "stderr": "",
                        "exit_code": "Timeout",
                        "compilation_time": compilation_time,
                        "execution_time": "N/A"
                    }

                    continue

                if compilation.returncode != 0:

                    if is_abnormal_termination(compilation.returncode):
                        status = "Compiler Crash"
                        print(f"{compiler.upper()}: Compiler crash detected!")

                    else:
                        status = "Compilation Failed"
                        print(f"{compiler.upper()}: Compilation failed.")

                    results[(compiler, optimization)] = {
                        "status": status,
                        "stdout": compilation.stdout,
                        "stderr": compilation.stderr,
                        "exit_code": compilation.returncode
                    }

                    continue

                print("Compilation successful")

                try:
                    execution_start = time.perf_counter()
                    execution = subprocess.run(
                        [executable],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    execution_time = time.perf_counter() - execution_start

                    print(f"Execution time: {execution_time:.6f} seconds")

                    if is_abnormal_termination(execution.returncode):

                        status = "Crash"
                        print(f"{compiler.upper()}: Abnormal termination detected!")

                    else:

                        status = "Success"
                        print(f"{compiler.upper()}: Execution completed.")

                    results[(compiler, optimization)] = {
                        "status": status,
                        "stdout": execution.stdout,
                        "stderr": execution.stderr,
                        "exit_code": execution.returncode,
                        "compilation_time": compilation_time,
                        "execution_time": execution_time
                    }

                    print("Program output:", repr(execution.stdout))
                    print("Execution exit code:", execution.returncode)
                except subprocess.TimeoutExpired:
                    print("Execution timed out!")

                    results[(compiler, optimization)] = {
                        "status": "Timeout",
                        "stdout": "",
                        "stderr": "",
                        "exit_code": "Timeout",
                        "compilation_time": compilation_time,
                        "execution_time": 5.0
                    }

            except FileNotFoundError:
                print(f"{compiler.upper()} was not found.")

                results[(compiler, optimization)] = {
                    "status": "Compiler not found",
                    "stdout": "",
                    "stderr": "",
                    "exit_code": "N/A",
                    "compilation_time": compilation_time,
                    "execution_time": "N/A"
                }

    # Compare GCC and Clang results
    
    # Compare all compiler and optimization combinations

    print("\n--- OPTIMIZATION COMPARISON ---")

    if all(
        result["status"] == "Success"
        for result in results.values()
    ):
        successful_results = list(results.values())

        reference = successful_results[0]

        all_match = all(
            result["stdout"] == reference["stdout"]
            and result["stderr"] == reference["stderr"]
            and result["exit_code"] == reference["exit_code"]
            for result in successful_results
        )

        comparison = "Match" if all_match else "Difference detected"

    else:
        comparison = "Comparison incomplete"

    print(comparison)

    # Save results to CSV

    report_file = "results/comparison_report.csv"
    file_exists = os.path.isfile(report_file)

    with open(report_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Input File",
                "Mutation",
                "Compiler",
                "Optimization",
                "Status",
                "Output",
                "Exit Code",
                "Comparison",
                "Compilation Time (seconds)",
                "Execution Time (seconds)"
            ])

        for (compiler, optimization), result in results.items():

            writer.writerow([
                input_file,
                mutation_name,
                compiler,
                optimization,
                result["status"],
                result["stdout"],
                result["exit_code"],
                comparison,
                result["compilation_time"],
                result["execution_time"]
            ])

    print(f"Results saved to {report_file}")
