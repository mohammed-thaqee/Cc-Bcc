
import random
from pycparser import c_parser, c_generator
from compiler_test import test_compilers
from mutations.mutate import build_symbol_table, replace_operator_type_aware

from mutations.mutate import (
    replace_constant_type_aware,
    build_symbol_table,
    replace_constant,
    replace_operator,
    duplicate_statement,
    delete_statement
)

# Read C source
# Available input programs
input_files = [
    "inputs/sample.c",
    "inputs/sample2.c",
    "inputs/sample3.c",
    "inputs/sample4.c"
]

# Randomly select an input program
selected_file = random.choice(input_files)

# selected_file = "inputs/sample2.c"

print(f"Selected input: {selected_file}")

# Read selected program
with open(selected_file, "r") as file:
    code = file.read()

# Parse into AST
parser = c_parser.CParser()
ast = parser.parse(code)

symbol_table = build_symbol_table(ast)
print("Symbol Table:", symbol_table)

# Available mutation operators
mutations = [
    replace_constant,
    replace_operator,
    duplicate_statement,
    delete_statement
]

# Randomly select a mutation
selected_mutation = random.choice(mutations)

# selected_mutation = replace_operator_type_aware


print(f"Selected mutation: {selected_mutation.__name__}")

# Apply mutation
ast = selected_mutation(ast, symbol_table)


# Generate modified C code
generator = c_generator.CGenerator()
mutated_code = generator.visit(ast)

# Save mutated program
with open("results/mutated.c", "w") as file:
    file.write(mutated_code)

print("\nMutated C program:")
print(mutated_code)

# Test generated program using GCC and Clang
test_compilers(
    "results/mutated.c",
    selected_file,
    selected_mutation.__name__
)