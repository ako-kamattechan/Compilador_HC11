from .ir import ModuloIR
from hc11cc.frontend.ast_nodes import Program


def build(ast: Program) -> ModuloIR:
    # Stub: convertir AST → IR
    return ModuloIR(funciones=[])
