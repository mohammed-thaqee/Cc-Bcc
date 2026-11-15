
import random
from pycparser import c_ast
import copy

def replace_constant(ast):

    constants = []

    # Find all integer constants in the AST
    class ConstantVisitor(c_ast.NodeVisitor):
        def visit_Constant(self, node):
            if node.type == "int":
                constants.append(node)

    visitor = ConstantVisitor()
    visitor.visit(ast)

    if not constants:
        print("No integer constants found.")
        return ast

    # Randomly select a constant
    selected = random.choice(constants)

    old_value = selected.value
    new_value = str(random.randint(1, 100))

    # Apply mutation
    selected.value = new_value

    print(f"Mutation: {old_value} -> {new_value}")

    return ast


def replace_operator(ast):

    operators = []

    # Find all arithmetic operations
    class OperatorVisitor(c_ast.NodeVisitor):
        def visit_BinaryOp(self, node):
            if node.op in ["+", "-", "*", "/"]:
                operators.append(node)

            self.generic_visit(node)

    visitor = OperatorVisitor()
    visitor.visit(ast)

    if not operators:
        print("No arithmetic operators found.")
        return ast

    # Select a random arithmetic operation
    selected = random.choice(operators)

    old_operator = selected.op

    possible_operators = ["+", "-", "*", "/"]
    possible_operators.remove(old_operator)

    new_operator = random.choice(possible_operators)

    # Apply mutation
    selected.op = new_operator

    print(f"Operator mutation: {old_operator} -> {new_operator}")

    return ast


def duplicate_statement(ast):

    main_function = None

    # Find the main function definition
    for node in ast.ext:
        if isinstance(node, c_ast.FuncDef) and node.decl.name == "main":
            main_function = node
            break

    if main_function is None:
        print("Main function not found.")
        return ast

    statements = main_function.body.block_items

    if not statements:
        print("No statements available.")
        return ast

    assignments = [
        stmt for stmt in statements
        if isinstance(stmt, c_ast.Assignment)
    ]

    if not assignments:
        print("No assignment statements available.")
        return ast

    selected = random.choice(assignments)
    index = statements.index(selected)

    duplicated = copy.deepcopy(selected)

    statements.insert(index + 1, duplicated)

    print("Statement duplicated.")

    return ast



def delete_statement(ast):

    main_function = None

    # Find the main function definition
    for node in ast.ext:
        if isinstance(node, c_ast.FuncDef) and node.decl.name == "main":
            main_function = node
            break

    if main_function is None:
        print("Main function not found.")
        return ast

    statements = main_function.body.block_items

    if not statements:
        print("No statements available.")
        return ast

    assignments = [
        stmt for stmt in statements
        if isinstance(stmt, c_ast.Assignment)
    ]

    if not assignments:
        print("No assignment statements available.")
        return ast

    selected = random.choice(assignments)

    statements.remove(selected)

    print("Assignment statement deleted.")

    return ast
