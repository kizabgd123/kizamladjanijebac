"""Unit tests for AST policy sandbox and Code as Policies (CaP) enforcement."""

import pytest
from src.core.ast_sandbox import ASTPolicyValidator, execute_policy_code, validate_python_code


def test_allow_safe_constructs():
    safe_code = """
items = [1, 2, 3, 4, 5]
squared = [x * x for x in items if x % 2 == 1]
result = {"sum": sum(squared), "count": len(squared)}
"""
    violations = validate_python_code(safe_code)
    assert len(violations) == 0

    res = execute_policy_code(safe_code)
    assert res.success is True
    assert res.output == {"sum": 35, "count": 3}
    assert res.error is None


def test_reject_import():
    code = "import os\nos.system('ls')"
    violations = validate_python_code(code)
    assert any("Forbidden Import" in v for v in violations)

    res = execute_policy_code(code)
    assert res.success is False
    assert "SecurityViolationError" in res.error


def test_reject_import_from():
    code = "from subprocess import run\nrun(['whoami'])"
    violations = validate_python_code(code)
    assert any("Forbidden ImportFrom" in v for v in violations)

    res = execute_policy_code(code)
    assert res.success is False
    assert "SecurityViolationError" in res.error


def test_reject_exec_and_eval():
    code_exec = "exec('x = 10')"
    assert len(validate_python_code(code_exec)) > 0
    res_exec = execute_policy_code(code_exec)
    assert res_exec.success is False

    code_eval = "eval('10 + 20')"
    assert len(validate_python_code(code_eval)) > 0
    res_eval = execute_policy_code(code_eval)
    assert res_eval.success is False


def test_reject_open_call():
    code = "f = open('/etc/passwd', 'r')"
    violations = validate_python_code(code)
    assert any("Forbidden function call: open()" in v for v in violations)

    res = execute_policy_code(code)
    assert res.success is False


def test_reject_dunder_attribute_traversal():
    code = "x = ().__class__.__bases__[0].__subclasses__()"
    violations = validate_python_code(code)
    assert any("Forbidden dunder attribute" in v for v in violations)

    res = execute_policy_code(code)
    assert res.success is False
    assert "SecurityViolationError" in res.error


def test_runtime_syntax_error():
    malformed_code = "def incomplete("
    violations = validate_python_code(malformed_code)
    assert any("SyntaxError" in v for v in violations)

    res = execute_policy_code(malformed_code)
    assert res.success is False
    assert "SyntaxError" in res.error
