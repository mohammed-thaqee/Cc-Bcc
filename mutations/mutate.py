
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



def build_symbol_table(ast):
    symbol_table = {}

    def get_type_name(type_node):

        if isinstance(type_node, c_ast.TypeDecl):
            base_type = get_type_name(type_node.type)

            if type_node.quals:
                qualifiers = " ".join(type_node.quals)
                return f"{qualifiers} {base_type}"

            return base_type

        elif isinstance(type_node, c_ast.IdentifierType):
            return " ".join(type_node.names)

        elif isinstance(type_node, c_ast.PtrDecl):
            return get_type_name(type_node.type) + " *"

        elif isinstance(type_node, c_ast.ArrayDecl):
            return get_type_name(type_node.type) + "[]"

        elif isinstance(type_node, c_ast.FuncDecl):
            return "function"

        elif isinstance(type_node, c_ast.Struct):
            if type_node.name:
                return f"struct {type_node.name}"
            return "anonymous struct"

        elif isinstance(type_node, c_ast.Union):
            if type_node.name:
                return f"union {type_node.name}"
            return "anonymous union"

        elif isinstance(type_node, c_ast.Enum):
            if type_node.name:
                return f"enum {type_node.name}"
            return "anonymous enum"

        return "unknown"

    class SymbolTableVisitor(c_ast.NodeVisitor):

        def visit_Decl(self, node):
            if node.name:
                symbol_table[node.name] = get_type_name(node.type)

            self.generic_visit(node)

        def visit_Typedef(self, node):
            symbol_table[node.name] = get_type_name(node.type)
            self.generic_visit(node)

    visitor = SymbolTableVisitor()
    visitor.visit(ast)

    return symbol_table


def replace_constant_type_aware(ast, symbol_table):

    replacements = []

    class ConstantVisitor(c_ast.NodeVisitor):

        def visit_Decl(self, node):
            if node.init is not None:
                if isinstance(node.init, c_ast.Constant):
                    var_type = symbol_table.get(node.name, "unknown")

                    replacements.append((node.init, var_type))

            self.generic_visit(node)

    visitor = ConstantVisitor()
    visitor.visit(ast)

    if not replacements:
        print("No suitable constants found.")
        return ast

    constant, var_type = random.choice(replacements)

    if "char" in var_type:
        constant.type = "char"
        constant.value = repr(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    elif "float" in var_type or "double" in var_type:
        constant.type = "float"
        constant.value = str(round(random.uniform(1.0, 100.0), 2))

    elif any(word in var_type for word in
             ["int", "short", "long", "signed", "unsigned"]):
        constant.type = "int"
        constant.value = str(random.randint(1, 100))

    else:
        print(f"Unsupported type: {var_type}")
        return ast

    print(f"Type-aware mutation: {var_type} constant replaced with {constant.value}")

    return ast
