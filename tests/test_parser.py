import pytest
import sys
import os

# Asegurar que src esté en el path si no está instalado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from hc11cc.frontend import (
    lex,
    parse,
    Program,
    Function,
    Return,
    IntLit,
    Let,
    Var,
    BinOp,
    BinOpKind,
    U8,
)
from hc11cc.errores import ErrorFrontend


def parse_code(code):
    tokens = lex(code)
    return parse(tokens)


def test_parser_basic_return():
    code = "fn main() -> u8 { return 7; }"
    program = parse_code(code)
    assert len(program.functions) == 1
    fn = program.functions[0]
    assert fn.name == "main"
    assert len(fn.body) == 1
    stmt = fn.body[0]
    assert isinstance(stmt, Return)
    assert isinstance(stmt.expr, IntLit)
    assert stmt.expr.val == 7


def test_parser_let_var():
    code = "fn main() -> u8 { let x: u8 = 10; return x; }"
    program = parse_code(code)
    fn = program.functions[0]
    assert len(fn.body) == 2
    let = fn.body[0]
    ret = fn.body[1]

    assert isinstance(let, Let)
    assert let.name == "x"
    assert isinstance(let.init, IntLit)
    assert let.init.val == 10

    assert isinstance(ret, Return)
    assert isinstance(ret.expr, Var)
    assert ret.expr.name == "x"


def test_parser_expr_precedence():
    code = "fn main() -> u8 { return 40 + 2 - 1; }"
    program = parse_code(code)
    # (40 + 2) - 1  (left associative)
    fn = program.functions[0]
    ret = fn.body[0]
    expr = ret.expr  # BinOp(-)

    assert isinstance(expr, BinOp)
    assert expr.op == BinOpKind.SUB
    assert isinstance(expr.rhs, IntLit)
    assert expr.rhs.val == 1

    lhs = expr.lhs  # BinOp(+)
    assert isinstance(lhs, BinOp)
    assert lhs.op == BinOpKind.ADD
    assert isinstance(lhs.lhs, IntLit)
    assert lhs.lhs.val == 40
    assert isinstance(lhs.rhs, IntLit)
    assert lhs.rhs.val == 2


def test_parser_parentheses():
    code = "fn main() -> u8 { return (40 + 2); }"
    program = parse_code(code)
    ret = program.functions[0].body[0]
    # (40+2) is just the BinOp
    expr = ret.expr
    assert isinstance(expr, BinOp)
    assert expr.op == BinOpKind.ADD


def test_parser_error_missing_semicolon():
    code = "fn main() -> u8 { return 7 }"  # Missing ;
    with pytest.raises(ErrorFrontend) as exc:
        parse_code(code)
    assert "Se esperaba SEMICOLON" in str(exc.value)


def test_parser_error_missing_type():
    # Faltante de anotación de tipo explícita para variable
    # Aunque la gramática requiere `let x: u8 = ...`
    code = "fn main() -> u8 { let x = 10; }"
    with pytest.raises(ErrorFrontend) as exc:
        parse_code(code)
    assert "Se esperaba COLON" in str(exc.value)


def test_parse_source_api():
    from hc11cc.frontend import parse_source

    code = "fn main() -> u8 { return 0; }"
    program = parse_source(code)
    assert isinstance(program, Program)
    assert len(program.functions) == 1
