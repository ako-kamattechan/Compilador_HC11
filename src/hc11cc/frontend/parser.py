from dataclasses import dataclass
from .lexer import Token
from hc11cc.errores import ErrorFrontend


@dataclass
class ASTPrograma:
    # placeholder
    funciones: list


def parse(tokens: list[Token]) -> ASTPrograma:
    if not tokens or tokens[-1].tipo != "EOF":
        raise ErrorFrontend("Tokens inválidos (falta EOF)")
    return ASTPrograma(funciones=[])
