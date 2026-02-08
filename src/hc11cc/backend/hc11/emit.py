from .isa import AsmProgram


def emit_asm(prog: AsmProgram) -> str:
    return "\n".join(prog.lineas) + "\n"
