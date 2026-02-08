from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class Span:
    """Representa un rango en el código fuente."""

    start: int  # offset de byte 0-indexado
    end: int  # offset de byte 0-indexado (exclusivo)
    line: int  # número de línea 1-indexado
    col: int  # número de columna 1-indexado

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError(f"Span inválido: end ({self.end}) < start ({self.start})")

    def __repr__(self):
        return f"Span({self.line}:{self.col})"


class TokenKind(Enum):
    # Palabras Clave
    FN = auto()
    MAIN = auto()
    LET = auto()
    RETURN = auto()
    U8 = auto()  # Tipo u8

    # Símbolos
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    SEMICOLON = auto()  # ;
    COLON = auto()  # :
    ASSIGN = auto()  # =
    PLUS = auto()  # +
    MINUS = auto()  # -
    ARROW = auto()  # ->

    # Literales e Identificadores
    IDENT = auto()  # ej. x, mi_var
    INT_LIT = auto()  # ej. 123

    # Control
    EOF = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    span: Span
    value: int | None = None  # Para INT_LIT

    def __repr__(self):
        if self.value is not None:
            return (
                f"Token({self.kind.name}, '{self.lexeme}', {self.value}, {self.span})"
            )
        return f"Token({self.kind.name}, '{self.lexeme}', {self.span})"
