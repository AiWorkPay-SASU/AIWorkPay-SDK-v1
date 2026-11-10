"""Les exemples du dépôt compilent et n'appellent que des méthodes qui existent."""
import ast
import pathlib

import pytest

import aiworkpay

EXAMPLES = sorted((pathlib.Path(__file__).parent.parent / "examples").glob("*.py"))


def test_there_are_examples():
    assert len(EXAMPLES) >= 4


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_example_compiles_and_uses_real_api(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "aiworkpay":
            for alias in node.names:
                assert hasattr(aiworkpay, alias.name), f"{path.name}: aiworkpay.{alias.name} n'existe pas"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id == "client":
                assert hasattr(aiworkpay.AIWorkPay, node.func.attr), f"{path.name}: client.{node.func.attr}"
                assert hasattr(aiworkpay.AsyncAIWorkPay, node.func.attr), f"{path.name}: async client.{node.func.attr}"
