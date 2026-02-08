from .tokens import Token, TokenKind, Span
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
from hc11cc.errores import ErrorFrontend


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        # Should not happen if EOF is present, but safe fallback
        return self.tokens[-1]

    def advance(self) -> Token:
        t = self.current()
        if self.pos < len(self.tokens):
            self.pos += 1
        return t

    def expect(self, kind: TokenKind) -> Token:
        t = self.current()
        if t.kind == kind:
            return self.advance()
        raise ErrorFrontend(f"Se esperaba {kind.name} se obtuvo {t.kind.name}", t.span)

    def parse_program(self) -> Program:
        functions = []
        while self.current().kind != TokenKind.EOF:
            functions.append(self.parse_function())
        return Program(functions)

    def parse_function(self) -> Function:
        self.expect(TokenKind.FN)
        if self.current().kind == TokenKind.MAIN:
            name_token = self.advance()
        else:
            name_token = self.expect(TokenKind.IDENT)

        self.expect(TokenKind.LPAREN)
        self.expect(TokenKind.RPAREN)

        # Tipo de retorno: -> u8
        # Opcional? El plan implica "-> u8" es parte de ello.
        # "Un solo main ... Retorno -> u8"
        # "fn main() -> u8"
        self.expect(TokenKind.ARROW)
        self.expect(TokenKind.U8)
        ret_ty = U8

        self.expect(TokenKind.LBRACE)
        body = []
        while (
            self.current().kind != TokenKind.RBRACE
            and self.current().kind != TokenKind.EOF
        ):
            body.append(self.parse_stmt())

        self.expect(TokenKind.RBRACE)
        return Function(name_token.lexeme, ret_ty, body)

    def parse_stmt(self) -> Stmt:
        if self.current().kind == TokenKind.LET:
            return self.parse_let()
        elif self.current().kind == TokenKind.RETURN:
            return self.parse_return()
        else:
            raise ErrorFrontend(
                f"Token inesperado para statement: {self.current().kind}",
                self.current().span,
            )

    def parse_let(self) -> Stmt:
        self.expect(TokenKind.LET)
        name = self.expect(TokenKind.IDENT).lexeme
        self.expect(TokenKind.COLON)
        self.expect(TokenKind.U8)  # Only u8 supported
        self.expect(TokenKind.ASSIGN)
        expr = self.parse_expr()
        self.expect(TokenKind.SEMICOLON)
        return Let(name, U8, expr)

    def parse_return(self) -> Stmt:
        self.expect(TokenKind.RETURN)
        expr = self.parse_expr()
        self.expect(TokenKind.SEMICOLON)
        return Return(expr)

    def parse_expr(self) -> Expr:
        # Expr -> Term { (+|-) Term }
        # Term -> Factor
        # So Expr -> Factor { (+|-) Factor } since we only have + - at same level
        lhs = self.parse_factor()

        while self.current().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op_token = self.advance()
            rhs = self.parse_factor()
            kind = BinOpKind.ADD if op_token.kind == TokenKind.PLUS else BinOpKind.SUB
            lhs = BinOp(kind, lhs, rhs)

        return lhs

    def parse_factor(self) -> Expr:
        t = self.current()
        if t.kind == TokenKind.INT_LIT:
            self.advance()
            return IntLit(t.value)
        elif t.kind == TokenKind.IDENT:
            self.advance()
            return Var(t.lexeme)
        elif t.kind == TokenKind.LPAREN:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenKind.RPAREN)
            return expr
        else:
            raise ErrorFrontend(f"Token inesperado en expresión: {t.kind}", t.span)


def parse(tokens: list[Token]) -> Program:
    parser = Parser(tokens)
    return parser.parse_program()
