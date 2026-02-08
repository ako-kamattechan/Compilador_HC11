import pytest
from hc11cc.frontend.lexer import lex
from hc11cc.frontend.parser import parse
from hc11cc.ir.builder import build


@pytest.mark.ir
def test_ir_smoke(ejemplo_minimo):
    ast = parse(lex(ejemplo_minimo))
    mod = build(ast)
    assert hasattr(mod, "funciones")
