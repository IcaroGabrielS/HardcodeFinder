import ast
def _is_literal_node_python(node):
    """
    Checks if a Python AST node represents a simple literal value or a collection of literals.
    (Internal helper function)
    """
    if isinstance(node, ast.Constant): 
        return True
    if isinstance(node, (ast.Str, ast.Num, ast.Bytes, ast.NameConstant)):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(_is_literal_node_python(el) for el in node.elts)
    if isinstance(node, ast.Dict):
        return all(_is_literal_node_python(k) and _is_literal_node_python(v) 
                   for k, v in zip(node.keys, node.values) if k is not None)
    return False
def _get_value_representation_python(node):
    """
    Tries to get a string representation of the Python AST node's value.
    (Internal helper function)
    """
    if hasattr(ast, 'unparse'): 
        try:
            return ast.unparse(node)
        except Exception: 
            pass 
    if isinstance(node, ast.Constant): return repr(node.value)
    if isinstance(node, ast.Str): return repr(node.s)
    if isinstance(node, ast.Num): return repr(node.n)
    if isinstance(node, ast.NameConstant): return repr(node.value)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        elements_repr = [_get_value_representation_python(el) for el in node.elts]
        if isinstance(node, ast.List): return f"[{', '.join(elements_repr)}]"
        if isinstance(node, ast.Tuple): return f"({', '.join(elements_repr)})" 
        if isinstance(node, ast.Set): return f"{{{', '.join(elements_repr)}}}"
    if isinstance(node, ast.Dict):
        pairs = []
        for k, v in zip(node.keys, node.values):
            if k is not None:
                 key_repr = _get_value_representation_python(k)
                 value_repr = _get_value_representation_python(v)
                 pairs.append(f"{key_repr}: {value_repr}")
        return f"{{{', '.join(pairs)}}}"
    return "<complex_value>"

class _PythonHardcodedFinderVisitor(ast.NodeVisitor):
    """
    AST Visitor for finding hardcoded variables in Python code.
    (Internal class)
    """
    def __init__(self):
        self.hardcoded_vars = []

    def visit_Assign(self, node):
        if _is_literal_node_python(node.value):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.hardcoded_vars.append({
                        "line": node.lineno,
                        "variable": target.id,
                        "value": _get_value_representation_python(node.value)
                    })
        self.generic_visit(node)
        
    def visit_AnnAssign(self, node):
        if node.value and _is_literal_node_python(node.value): 
            if isinstance(node.target, ast.Name):
                self.hardcoded_vars.append({
                    "line": node.lineno,
                    "variable": node.target.id,
                    "value": _get_value_representation_python(node.value)
                })
        self.generic_visit(node)

def find_hardcoded_in_python_file(filepath):
    """
    Analyzes a single Python file for hardcoded variables using AST.
    Returns a list of dictionaries with found variables, or an empty list if none found.
    Returns None if a file processing error (read, syntax) occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        tree = ast.parse(content, filename=filepath)
        finder_visitor = _PythonHardcodedFinderVisitor()
        finder_visitor.visit(tree)
        return finder_visitor.hardcoded_vars
    except FileNotFoundError:
        print(f"Error [Python Analyzer]: File '{filepath}' not found.")
        return None
    except SyntaxError as e:
        print(f"Syntax error [Python Analyzer] in '{filepath}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error [Python Analyzer] processing '{filepath}': {e}")
        return None
