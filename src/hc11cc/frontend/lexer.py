from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    tipo: str
    lexema: str


def lex(codigo: str) -> list[Token]:
    # Stub mínimo: devolver EOF para que el pipeline no explote.
    return [Token("EOF", "")]
