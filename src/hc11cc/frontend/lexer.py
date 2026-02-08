from .tokens import Token, TokenKind, Span
from hc11cc.errores import ErrorFrontend


def lex(source: str) -> list[Token]:
    tokens = []
    i = 0
    n = len(source)
    line = 1
    col = 1

    # Helper para avanzar
    def advance(amount=1):
        nonlocal i, col
        i += amount
        col += amount

    # Helper para rastrear saltos de línea
    def newline():
        nonlocal line, col
        line += 1
        col = 1

    KEYWORDS = {
        "fn": TokenKind.FN,
        "main": TokenKind.MAIN,
        "let": TokenKind.LET,
        "return": TokenKind.RETURN,
        "u8": TokenKind.U8,
    }

    while i < n:
        char = source[i]

        # Espacios en blanco
        if char in " \t\r":
            advance()
        elif char == "\n":
            i += 1
            newline()

        # Símbolos
        elif char == "(":
            tokens.append(Token(TokenKind.LPAREN, "(", Span(i, i + 1, line, col)))
            advance()
        elif char == ")":
            tokens.append(Token(TokenKind.RPAREN, ")", Span(i, i + 1, line, col)))
            advance()
        elif char == "{":
            tokens.append(Token(TokenKind.LBRACE, "{", Span(i, i + 1, line, col)))
            advance()
        elif char == "}":
            tokens.append(Token(TokenKind.RBRACE, "}", Span(i, i + 1, line, col)))
            advance()
        elif char == ";":
            tokens.append(Token(TokenKind.SEMICOLON, ";", Span(i, i + 1, line, col)))
            advance()
        elif char == ":":
            tokens.append(Token(TokenKind.COLON, ":", Span(i, i + 1, line, col)))
            advance()
        elif char == "=":
            tokens.append(Token(TokenKind.ASSIGN, "=", Span(i, i + 1, line, col)))
            advance()
        elif char == "+":
            tokens.append(Token(TokenKind.PLUS, "+", Span(i, i + 1, line, col)))
            advance()
        elif char == "-":
            # Revisar si es ->
            if i + 1 < n and source[i + 1] == ">":
                tokens.append(Token(TokenKind.ARROW, "->", Span(i, i + 2, line, col)))
                advance(2)
            else:
                tokens.append(Token(TokenKind.MINUS, "-", Span(i, i + 1, line, col)))
                advance()

        # Identificadores y Palabras Clave
        elif char.isalpha() or char == "_":
            start_i = i
            start_col = col
            lexeme = char
            advance()
            while i < n and (source[i].isalnum() or source[i] == "_"):
                lexeme += source[i]
                advance()

            kind = KEYWORDS.get(lexeme, TokenKind.IDENT)
            tokens.append(Token(kind, lexeme, Span(start_i, i, line, start_col)))

        # Enteros (decimales)
        elif char.isdigit():
            start_i = i
            start_col = col
            lexeme = char
            advance()
            while i < n and source[i].isdigit():
                lexeme += source[i]
                advance()

            tokens.append(
                Token(
                    TokenKind.INT_LIT,
                    lexeme,
                    Span(start_i, i, line, start_col),
                    int(lexeme),
                )
            )

        else:
            raise ErrorFrontend(
                f"Caracter inesperado '{char}'", Span(i, i + 1, line, col)
            )

    tokens.append(Token(TokenKind.EOF, "", Span(n, n, line, col)))
    return tokens
