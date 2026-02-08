from .ir import ModuloIR
from hc11cc.frontend.parser import ASTPrograma


def build(ast: ASTPrograma) -> ModuloIR:
    # Stub: convertir AST → IR
    return ModuloIR(funciones=[])
