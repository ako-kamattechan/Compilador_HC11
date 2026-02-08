from .tokens import Token, TokenKind, Span
from .lexer import lex
from .parser import parse
from .ast_nodes import (
    Program,
    Function,
    Stmt,
    Let,
    Return,
    Expr,
    IntLit,
    Var,
    BinOp,
    BinOpKind,
    Type,
    U8,
)


def parse_source(source: str) -> Program:
    tokens = lex(source)
    return parse(tokens)
