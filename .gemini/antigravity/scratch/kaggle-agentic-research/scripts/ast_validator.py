#!/usr/bin/env python3
"""
AST Security & Integrity Validator
==================================
Performs static Abstract Syntax Tree (AST) analysis on Python scripts before
execution. Blocks dangerous system calls, unauthorized networking, arbitrary
code execution primitives, and structural integrity violations.
"""

import ast
import sys
import os
from typing import List, Dict, Any, Optional, Set

DEFAULT_BANNED_MODULES = {
    "subprocess",
    "pty",
    "socket",
    "urllib",
    "requests",
    "aiohttp",
    "httpx",
    "http",
    "ctypes",
    "sys.setrecursionlimit",
    "importlib",
    "multiprocessing",
}

DEFAULT_BANNED_CALLS = {
    "eval",
    "exec",
    "compile",
    "breakpoint",
    "fork",
}

DEFAULT_BANNED_ATTRIBUTES = {
    "system",
    "popen",
    "spawn",
    "spawnl",
    "spawnle",
    "spawnv",
    "spawnve",
    "rmdir",
    "rmtree",
    "unlink",
    "remove",
}

SUSPICIOUS_DUNDERS = {
    "__subclasses__",
    "__globals__",
    "__code__",
    "__builtins__",
    "__class__",
}


class ASTSecurityVisitor(ast.NodeVisitor):
    def __init__(
        self,
        banned_modules: Optional[Set[str]] = None,
        banned_calls: Optional[Set[str]] = None,
        banned_attrs: Optional[Set[str]] = None,
        allow_network: bool = False,
    ):
        self.banned_modules = set(banned_modules or DEFAULT_BANNED_MODULES)
        if allow_network:
            self.banned_modules -= {"requests", "httpx", "aiohttp", "urllib", "http", "socket"}
            
        self.banned_calls = set(banned_calls or DEFAULT_BANNED_CALLS)
        self.banned_attrs = set(banned_attrs or DEFAULT_BANNED_ATTRIBUTES)
        self.violations: List[Dict[str, Any]] = []

    def _add_violation(self, node: ast.AST, code: str, message: str):
        line = getattr(node, "lineno", 0)
        col = getattr(node, "col_offset", 0)
        self.violations.append({
            "code": code,
            "message": message,
            "line": line,
            "col": col,
        })

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module in self.banned_modules or alias.name in self.banned_modules:
                self._add_violation(
                    node,
                    "SEC_BANNED_IMPORT",
                    f"Forbidden import: '{alias.name}'"
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module in self.banned_modules or node.module in self.banned_modules:
                self._add_violation(
                    node,
                    "SEC_BANNED_IMPORT",
                    f"Forbidden from-import module: '{node.module}'"
                )
        for alias in node.names:
            full_name = f"{node.module}.{alias.name}" if node.module else alias.name
            if full_name in self.banned_modules or alias.name in self.banned_calls:
                self._add_violation(
                    node,
                    "SEC_BANNED_IMPORT",
                    f"Forbidden imported symbol: '{full_name}'"
                )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Direct function call: eval(), exec(), compile()
        if isinstance(node.func, ast.Name):
            if node.func.id in self.banned_calls:
                self._add_violation(
                    node,
                    "SEC_BANNED_CALL",
                    f"Dangerous built-in function called: '{node.func.id}()'"
                )
            elif node.func.id == "__import__":
                self._add_violation(
                    node,
                    "SEC_DYNAMIC_IMPORT",
                    "Dynamic built-in import '__import__()' is prohibited."
                )

        # Method call: os.system(), shutil.rmtree()
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if attr_name in self.banned_attrs:
                self._add_violation(
                    node,
                    "SEC_BANNED_METHOD",
                    f"Dangerous OS/system method called: '.{attr_name}()'"
                )
            elif attr_name in SUSPICIOUS_DUNDERS:
                self._add_violation(
                    node,
                    "SEC_INTROSPECTION_EVASION",
                    f"Suspicious dunder introspection attribute access: '{attr_name}'"
                )

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr in SUSPICIOUS_DUNDERS:
            self._add_violation(
                node,
                "SEC_INTROSPECTION_EVASION",
                f"Forbidden dunder attribute traversal: '{node.attr}'"
            )
        self.generic_visit(node)


def validate_python_code(
    code_str: str,
    allow_network: bool = False,
    extra_banned_modules: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    Parses and audits a Python source code string.
    Returns:
        dict: {'valid': bool, 'syntax_ok': bool, 'violations': list, 'error': str|None}
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {
            "valid": False,
            "syntax_ok": False,
            "violations": [{
                "code": "SYNTAX_ERROR",
                "message": f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}",
                "line": e.lineno or 0,
                "col": e.offset or 0,
            }],
            "error": str(e),
        }

    visitor = ASTSecurityVisitor(
        banned_modules=extra_banned_modules,
        allow_network=allow_network,
    )
    visitor.visit(tree)

    is_valid = len(visitor.violations) == 0
    return {
        "valid": is_valid,
        "syntax_ok": True,
        "violations": visitor.violations,
        "error": None if is_valid else f"Found {len(visitor.violations)} AST violation(s)",
    }


def validate_python_file(
    file_path: str,
    allow_network: bool = False,
) -> Dict[str, Any]:
    """Reads and validates a Python source file from disk."""
    if not os.path.exists(file_path):
        return {
            "valid": False,
            "syntax_ok": False,
            "violations": [{
                "code": "FILE_NOT_FOUND",
                "message": f"File does not exist: {file_path}",
                "line": 0,
                "col": 0,
            }],
            "error": "File does not exist",
        }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {
            "valid": False,
            "syntax_ok": False,
            "violations": [{
                "code": "READ_ERROR",
                "message": f"Could not read file: {e}",
                "line": 0,
                "col": 0,
            }],
            "error": str(e),
        }

    result = validate_python_code(content, allow_network=allow_network)
    result["file"] = file_path
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ast_validator.py <script.py> [--allow-network]")
        sys.exit(1)

    filepath = sys.argv[1]
    allow_net = "--allow-network" in sys.argv

    result = validate_python_file(filepath, allow_network=allow_net)
    if result["valid"]:
        print(f"✅ AST VALIDATION PASSED: '{filepath}' is clean.")
        sys.exit(0)
    else:
        print(f"❌ AST VALIDATION FAILED: '{filepath}' has violations:")
        for v in result["violations"]:
            print(f"   • Line {v['line']}:{v['col']} [{v['code']}]: {v['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
