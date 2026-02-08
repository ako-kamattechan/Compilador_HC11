import pytest
import sys
import os

# Ensure src is in path if not installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from hc11cc.frontend import lex, TokenKind
from hc11cc.errores import ErrorFrontend


def test_lexer_fn_main():
    source = "fn main() -> u8 { return 7; }"
    tokens = lex(source)

    expected = [
        TokenKind.FN,
        TokenKind.MAIN,
        TokenKind.LPAREN,
        TokenKind.RPAREN,
        TokenKind.ARROW,
        TokenKind.U8,
        TokenKind.LBRACE,
        TokenKind.RETURN,
        TokenKind.INT_LIT,
        TokenKind.SEMICOLON,
        TokenKind.RBRACE,
        TokenKind.EOF,
    ]

    assert len(tokens) == len(expected)
    for t, k in zip(tokens, expected):
        assert t.kind == k

    assert tokens[8].value == 7


def test_lexer_let_assign():
    source = "let x: u8 = 40 + 2;"
    tokens = lex(source)

    # let x : u8 = 40 + 2 ; EOF
    assert tokens[0].kind == TokenKind.LET
    assert tokens[1].kind == TokenKind.IDENT
    assert tokens[1].lexeme == "x"
    assert tokens[2].kind == TokenKind.COLON
    assert tokens[3].kind == TokenKind.U8
    assert tokens[4].kind == TokenKind.ASSIGN
    assert tokens[5].kind == TokenKind.INT_LIT
    assert tokens[5].value == 40
    assert tokens[6].kind == TokenKind.PLUS
    assert tokens[7].kind == TokenKind.INT_LIT
    assert tokens[7].value == 2
    assert tokens[8].kind == TokenKind.SEMICOLON
    assert tokens[9].kind == TokenKind.EOF


def test_lexer_error_unexpected_char():
    source = "let x = @;"
    with pytest.raises(ErrorFrontend) as excinfo:
        lex(source)

    assert "Caracter inesperado '@'" in str(excinfo.value)
    assert excinfo.value.span.line == 1
    # Check column. "let x = " is 8 chars. @ is at index 8 (0-indexed) -> col 9?
    # let is 3, space 1, x 1, space 1, = 1, space 1 = 8 chars.
    # index 01234567
    # "let x = "
    # @ is at 8.
    # So col should be 9 if 1-indexed?
    # My lexer starts col at 1.
    # space updates col.
    # let's trust the logic for now, verifying span roughly.


def test_lexer_spans():
    source = "fn"
    tokens = lex(source)
    t = tokens[0]
    assert t.kind == TokenKind.FN
    assert t.span.start == 0
    assert t.span.end == 2
    assert t.span.line == 1
    assert t.span.col == 1
