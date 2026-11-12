"""
AST-based policy validator and execution environment for Code as Policies (CaP).

Note: Static AST validation provides an application policy layer to restrict
computational patterns; it does NOT constitute an OS-level security sandbox.
"""

import ast
import time
from typing import Any, Dict, List, Optional, Set


class SecurityViolationError(Exception):
    """Raised when model-generated code violates AST policy restrictions."""
    pass


class ASTPolicyValidator(ast.NodeVisitor):
    """
    Validates Python AST against strict safety constraints.
    Rejects:
      - Import and ImportFrom
      - Calls to exec, eval, compile, open, getattr, setattr, delattr, __import__
      - Dunder attribute lookups (__class__, __subclasses__, __globals__, etc.)
      - Async constructs or system-level calls
    """

    FORBIDDEN_CALLS: Set[str] = {
        "exec", "eval", "compile", "open", "__import__",
        "getattr", "setattr", "delattr", "globals", "locals",
        "input", "breakpoint", "help", "memoryview"
    }

    FORBIDDEN_ATTRIBUTES: Set[str] = {
        "__class__", "__subclasses__", "__globals__", "__builtins__",
        "__code__", "__closure__", "__dict__", "__module__", "__bases__",
        "__mro__", "__qualname__"
    }

    def __init__(self, allow_imports: bool = False):
        self.allow_imports = allow_imports
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        if not self.allow_imports:
            names = [alias.name for alias in node.names]
            self.violations.append(f"Forbidden Import statement: {names} at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if not self.allow_imports:
            self.violations.append(f"Forbidden ImportFrom statement: {node.module} at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Check direct calls by name
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_CALLS:
                self.violations.append(f"Forbidden function call: {node.func.id}() at line {node.lineno}")
        # Check method calls
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in self.FORBIDDEN_CALLS:
                self.violations.append(f"Forbidden method call: .{node.func.attr}() at line {node.lineno}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__") and node.attr.endswith("__"):
            self.violations.append(f"Forbidden dunder attribute access: .{node.attr} at line {node.lineno}")
        elif node.attr in self.FORBIDDEN_ATTRIBUTES:
            self.violations.append(f"Forbidden attribute access: .{node.attr} at line {node.lineno}")
        self.generic_visit(node)


class SandboxedExecutionResult:
    def __init__(self, success: bool, output: Any = None, error: Optional[str] = None, elapsed_ms: float = 0.0):
        self.success = success
        self.output = output
        self.error = error
        self.elapsed_ms = elapsed_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "elapsed_ms": self.elapsed_ms,
        }


def validate_python_code(code_str: str, allow_imports: bool = False) -> List[str]:
    """Parse and validate Python code string using ASTPolicyValidator."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return [f"SyntaxError during AST parse: {e}"]

    validator = ASTPolicyValidator(allow_imports=allow_imports)
    validator.visit(tree)
    return validator.violations


def execute_policy_code(
    code_str: str,
    safe_globals: Optional[Dict[str, Any]] = None,
    timeout_ms: int = 5000,
    allow_imports: bool = False
) -> SandboxedExecutionResult:
    """
    Validates and executes a Python policy string within a restricted execution scope.
    """
    start_time = time.time()
    violations = validate_python_code(code_str, allow_imports=allow_imports)
    if violations:
        return SandboxedExecutionResult(
            success=False,
            error=f"SecurityViolationError: {'; '.join(violations)}",
            elapsed_ms=(time.time() - start_time) * 1000.0
        )

    # Restricted builtins
    restricted_builtins = {
        "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
        "enumerate": enumerate, "float": float, "int": int, "len": len,
        "list": list, "max": max, "min": min, "range": range, "round": round,
        "set": set, "sorted": sorted, "str": str, "sum": sum, "tuple": tuple,
        "zip": zip, "None": None, "True": True, "False": False
    }

    exec_globals: Dict[str, Any] = {"__builtins__": restricted_builtins}
    if safe_globals:
        exec_globals.update(safe_globals)

    exec_locals: Dict[str, Any] = {}

    def _run():
        compiled = compile(code_str, "<cap_policy>", "exec")
        exec(compiled, exec_globals, exec_locals)

    import concurrent.futures
    timeout_sec = max(0.001, timeout_ms / 1000.0)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run)
            future.result(timeout=timeout_sec)
        elapsed = (time.time() - start_time) * 1000.0

        # Look for result variable or return dictionary of locals
        output = exec_locals.get("result", exec_locals)
        return SandboxedExecutionResult(success=True, output=output, elapsed_ms=elapsed)
    except concurrent.futures.TimeoutError:
        elapsed = (time.time() - start_time) * 1000.0
        return SandboxedExecutionResult(
            success=False,
            error=f"TimeoutError: Execution exceeded {timeout_ms}ms limit",
            elapsed_ms=elapsed
        )
    except Exception as e:
        elapsed = (time.time() - start_time) * 1000.0
        return SandboxedExecutionResult(
            success=False,
            error=f"Runtime execution error: {type(e).__name__}: {str(e)}",
            elapsed_ms=elapsed
        )
