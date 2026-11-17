# GrayC-Inspired Compiler Fuzzing Framework

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![C](https://img.shields.io/badge/Language-C-blue)
![GCC](https://img.shields.io/badge/Compiler-GCC-red?logo=gnu)
![Clang](https://img.shields.io/badge/Compiler-Clang-orange?logo=llvm)
![AST](https://img.shields.io/badge/Approach-AST--Based-purple)
![Status](https://img.shields.io/badge/Project-In%20Development-yellow)

An AST-based compiler fuzzing prototype inspired by **GrayC: Greybox Fuzzing of Compilers and Analysers for C**.

The project aims to automatically generate mutated C programs, compile and execute them using multiple compilers, and compare their behaviour across different optimization levels. It explores AST-based mutation, basic type-guided transformations, and differential compiler testing.

---

## Overview

Compiler bugs can cause incorrect program execution, compilation failures, crashes, and inconsistencies across optimization levels.

This project implements a simplified compiler-testing framework that automates the generation and testing of modified C programs.

Using Python and `pycparser`, C programs are parsed into Abstract Syntax Trees (ASTs). The ASTs are then modified through different mutation operations before being converted back into C source code.

The generated programs are tested using GCC and Clang at four optimization levels:

- `-O0`
- `-O1`
- `-O2`
- `-O3`

The framework captures compilation and execution results, measures execution timings, detects common failures, and compares the observable behaviour of different compiler configurations.

The current implementation also introduces basic type-guided mutation techniques using symbol-table information.

## Key Features

### Implemented

- **AST-Based C Parsing:** Converts C source programs into Abstract Syntax Trees using `pycparser`.
- **AST Mutation:** Supports constant replacement, operator replacement, statement duplication, and statement deletion.
- **Type-Guided Mutation:** Uses a symbol table to guide constant and operator replacements based on approximate operand and variable types.
- **Multiple Compiler Support:** Tests generated programs using GCC and Clang.
- **Optimization-Level Testing:** Evaluates programs using `-O0`, `-O1`, `-O2`, and `-O3`.
- **Differential Testing:** Compares standard output, standard error, and exit codes across compiler configurations.
- **Performance Measurement:** Records compilation and execution times.
- **Timeout Detection:** Identifies compilation and execution timeouts.
- **Abnormal Termination Detection:** Detects common crash and abnormal termination indicators.
- **CSV Reporting:** Automatically records experimental results in a CSV report.

### Planned

- Coverage-guided fuzzing and feedback-based input selection.
- LibFuzzer integration.
- More comprehensive C semantic and type validation.
- Program recombination through function and code-fragment combination.
- Improved handling of undefined behaviour and invalid mutations.

---

## System Architecture

The current framework follows this pipeline:

```text
             C Input Programs
                    |
                    v
              AST Parsing
              (pycparser)
                    |
                    v
            Symbol Table Creation
                    |
                    v
              AST Mutation
                    |
          +---------+----------+
          |         |          |
          v         v          v
       Constant  Operator   Statement
       Mutation  Mutation   Duplication/
                            Deletion
          |         |          |
          +---------+----------+
                    |
                    v
             AST Code Generation
                    |
                    v
             Mutated C Program
                    |
                    v
           Compiler Testing Engine
                    |
             +------+------+
             |             |
             v             v
            GCC          Clang
             |             |
        -O0 to -O3    -O0 to -O3
             |             |
             +------+------+
                    |
                    v
          Compilation & Execution
                    |
                    v
          Result Collection and
             Comparison
                    |
                    v
              CSV Report
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Input Language | C |
| AST Parsing | pycparser |
| AST Generation | pycparser CGenerator |
| Compiler 1 | GCC |
| Compiler 2 | Clang |
| Process Management | Python subprocess |
| Performance Measurement | Python time |
| Result Storage | CSV |
| Development Environment | Visual Studio Code |

---

## Project Structure

```text
CD Project/
│
├── inputs/
│   ├── sample.c
│   ├── sample2.c
│   ├── sample3.c
│   ├── sample4.c
│   ├── datatype_test.c
│   ├── invalid.c
│   ├── infinite_loop.c
│   └── crash.c
│
├── mutations/
│   └── mutate.py
│
├── results/
│   ├── mutated.c
│   ├── comparison_report.csv
│   └── compiler executables
│
├── main.py
├── compiler_test.py
├── test_invalid.py
├── test_timeout.py
├── test_crash.py
├── requirements.txt
│
└── README.md
```

### Directory Description

| Directory/File | Description |
|---|---|
| `inputs/` | Contains original C programs used for testing and mutation. |
| `mutations/` | Contains AST mutation operations and symbol-table functionality. |
| `results/` | Stores generated C programs, compiler outputs, executables, and CSV reports. |
| `main.py` | Main execution entry point for parsing, mutation, and testing. |
| `compiler_test.py` | Handles GCC/Clang compilation, execution, and result comparison. |
| `test_invalid.py` | Tests invalid C program handling. |
| `test_timeout.py` | Tests execution timeout handling. |
| `test_crash.py` | Tests abnormal program termination detection. |
| `requirements.txt` | Contains Python dependencies. |

---

## AST Mutation Techniques

The framework currently implements four fundamental AST mutation operations.

### 1. Constant Replacement

Identifies constant nodes in the AST and replaces selected values with randomly generated alternatives.

Example:

**Original:**

```c
int a = 10;
```

**Mutated:**

```c
int a = 45;
```

A type-guided version has also been implemented for constants directly assigned during variable declarations.

### 2. Operator Replacement

Identifies binary arithmetic operators and replaces them with alternative operators.

Example:

**Original:**

```c
int result = a + b;
```

**Mutated:**

```c
int result = a * b;
```

### 3. Statement Duplication

Selects an assignment statement and duplicates it within the function body.

Example:

**Original:**

```c
result = result + 1;
```

**Mutated:**

```c
result = result + 1;
result = result + 1;
```

### 4. Statement Deletion

Selects an assignment statement and removes it from the AST.

This allows the framework to explore variations in program execution caused by the removal of individual statements.

---

## Type-Guided Mutation

A basic type-guided mutation mechanism has been introduced to improve the validity of generated programs.

### Symbol Table

The `build_symbol_table()` function traverses the AST and records variable names and their declared types.

Currently recognised categories include:

- Primitive types: `int`, `char`, `float`, `double`, `void`.
- Modified integer types: `unsigned`, `signed`, `short`, `long`.
- Pointers and multi-level pointers.
- Arrays and multidimensional arrays.
- Structures.
- Unions.
- Enumerations.
- Typedef declarations.

### Type-Aware Constant Replacement

The `replace_constant_type_aware()` function uses declared variable types to guide constant replacements.

Examples:

| Variable Type | Replacement Category |
|---|---|
| `int` | Integer values |
| `float` | Floating-point values |
| `double` | Floating-point values |
| `char` | Character values |

The current implementation focuses on direct declaration initializers.

### Type-Aware Operator Replacement

The `replace_operator_type_aware()` function examines the approximate types of binary expression operands before selecting alternative operators.

The implemented operator categories include:

| Category | Operators |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Relational | `<`, `>`, `<=`, `>=` |
| Equality | `==`, `!=` |
| Logical | `&&`, `||` |
| Bitwise | `&`, `|`, `^` |
| Shift | `<<`, `>>` |
| Pointer Arithmetic | `+`, `-` |

**Note:** The current implementation uses simplified type rules. It does not implement the complete C type system, integer promotions, usual arithmetic conversions, comprehensive pointer compatibility checks, or full undefined-behaviour validation. Type-guided mutations should therefore not be considered guaranteed to be semantically valid.

---

## Compiler Testing and Differential Comparison

Each generated C program is tested against two compilers:

- GCC
- Clang

Each compiler is tested using four optimization configurations.

| Compiler | Optimization Levels |
|---|---|
| GCC | `-O0`, `-O1`, `-O2`, `-O3` |
| Clang | `-O0`, `-O1`, `-O2`, `-O3` |

This produces eight compiler configurations for every test program.

### Comparison Criteria

The framework compares:

1. Standard output (`stdout`).
2. Standard error (`stderr`).
3. Program exit code.

The comparison produces one of three outcomes:

| Result | Meaning |
|---|---|
| `Match` | All eight configurations succeeded and produced identical observable results. |
| `Difference detected` | Successful configurations produced different observable results. |
| `Comparison incomplete` | One or more configurations failed, timed out, or terminated abnormally. |

A matching result indicates agreement among the tested configurations. It does not independently establish program correctness or compiler correctness.

### Failure and Timeout Handling

The framework includes:

- Compilation timeout: 10 seconds.
- Execution timeout: 5 seconds.
- Compilation failure detection.
- Basic compiler and program abnormal termination detection.
- Execution timeout detection.

Abnormal termination detection includes common POSIX signal return codes and selected Windows exception codes.

---

## Experimental Results

The framework has been tested using multiple input programs and AST mutations.

Some verified test outcomes include:

| Input | Mutation | Observed Result |
|---|---|---|
| `sample.c` | Statement duplication | Exit code: 32 |
| `sample2.c` | Statement duplication | Exit code: 20 |
| `sample3.c` | Statement duplication | Exit code: 80 |
| `sample4.c` | Constant replacement | Output: `91` in one test |
| `sample4.c` | Type-aware constant replacement | Output: `55` |
| `sample2.c` | Type-aware operator replacement | Exit code: 48 |
| `sample2.c` | Shift operator replacement | Exit code: `4294967294` on Windows |

The recorded successful tests showed matching observable results across GCC, Clang, and the tested optimization levels.

These are prototype validation results, not evidence of comprehensive compiler correctness or large-scale fuzzing effectiveness.

### CSV Reports

Experimental results are stored in:

```text
results/comparison_report.csv
```

The report records:

- Input filename.
- Mutation applied.
- Compiler.
- Optimization level.
- Compilation and execution status.
- Program output.
- Exit code.
- Comparison result.
- Compilation time.
- Execution time.

---

## Installation and Setup

### Prerequisites

Ensure the following are installed:

- Python 3.x
- GCC
- Clang
- Git

Both GCC and Clang must be accessible through the system PATH.

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify compiler installations

```bash
gcc --version
clang --version
```

---

## Running the Project

Execute the main script:

```bash
python main.py
```

The framework will:

1. Select an input C program.
2. Parse the program into an AST.
3. Construct the symbol table.
4. Select and apply a mutation.
5. Generate the mutated C program.
6. Compile the program using GCC and Clang.
7. Execute it under the four optimization levels.
8. Compare the results.
9. Save the experimental results to CSV.

Generated C programs are stored in:

```text
results/mutated.c
```

Experimental reports are stored in:

```text
results/comparison_report.csv
```

---

## Current Limitations

This project is an evolving prototype and has not yet implemented all the capabilities of the original GrayC framework.

The current limitations include:

- Mutation selection is random and does not use compiler coverage feedback.
- Type information is approximate and does not constitute complete semantic validation.
- Some mutations may introduce undefined behaviour or semantically invalid expressions.
- Symbol-table handling does not fully resolve variable scopes, shadowing, and typedef aliases.
- Pointer and complex expression compatibility rules are incomplete.
- Program recombination has not been implemented.
- LibFuzzer has not been integrated.
- Large-scale fuzzing experiments have not yet been conducted.

---

## Future Work

The following improvements are planned:

### 1. Coverage-Guided Fuzzing

Introduce compiler code-coverage feedback to identify mutations that exercise previously unexplored compiler execution paths.

Inputs that discover new coverage will be retained and used as candidates for subsequent mutations.

### 2. LibFuzzer Integration

Explore integration with LibFuzzer to support coverage-guided input generation and corpus evolution.

### 3. Improved Type-Aware Mutations

Extend the existing type-guided mutation system with more comprehensive C type analysis, semantic validation, and restrictions against invalid transformations.

### 4. Program Recombination

Implement the combination of functions and compatible code fragments from different C programs to generate more diverse test inputs.

### 5. Extended Testing and Evaluation

Conduct larger-scale experiments to evaluate:

- Number of generated test programs.
- Compilation success rate.
- Execution success rate.
- Unique compiler coverage.
- Crash and failure detection.
- Differences across compilers and optimization levels.

---

## Research Background

This project is inspired by the research paper:

**GrayC: Greybox Fuzzing of Compilers and Analysers for C**

The project explores a simplified implementation of selected concepts from GrayC, particularly AST-based program mutation and compiler testing.

It is an independent educational prototype developed as part of a Compiler Design project and is not an official implementation or reproduction of the original GrayC framework.

---

## Project Status

**Current stage:** Foundational AST-based mutation and differential compiler testing implemented.

The project is actively being extended with improved type-guided mutations, coverage-guided fuzzing, and program recombination.

---

## Keywords

`Compiler Design` `Compiler Testing` `Compiler Fuzzing` `AST` `Abstract Syntax Tree` `C Programming` `Python` `pycparser` `GCC` `Clang` `Differential Testing` `Type-Aware Mutation` `Software Testing` `Fuzz Testing` `Program Mutation` `Code Generation`
