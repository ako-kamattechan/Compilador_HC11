import pytest
from hc11cc.frontend.lexer import lex
from hc11cc.frontend.parser import parse
from hc11cc.frontend.sema import validar


@pytest.mark.frontend
def test_frontend_smoke(ejemplo_minimo):
    tokens = lex(ejemplo_minimo)
    ast = parse(tokens)
    validar(ast)
