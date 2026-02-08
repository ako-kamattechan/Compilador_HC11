from hc11cc.config import Config
from hc11cc.frontend.lexer import lex
from hc11cc.frontend.parser import parse
from hc11cc.frontend.sema import validar
from hc11cc.ir.builder import build
from hc11cc.ir.emit import emit_ir
from hc11cc.backend.hc11.isel import seleccionar
from hc11cc.backend.hc11.program import envolver_programa
from hc11cc.backend.hc11.emit import emit_asm


def compilar(codigo_fuente: str, cfg: Config | None = None) -> str:
    cfg = cfg or Config()

    tokens = lex(codigo_fuente)
    ast = parse(tokens)
    validar(ast)

    modulo_ir = build(ast)

    if cfg.emitir_ir:
        return emit_ir(modulo_ir)

    instrs = seleccionar(modulo_ir)
    asm_prog = envolver_programa(instrs, cfg)
    return emit_asm(asm_prog)
