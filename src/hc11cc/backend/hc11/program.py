from hc11cc.config import Config
from .isa import AsmProgram


def envolver_programa(instrs: list[str], cfg: Config) -> AsmProgram:
    # Stub: prologo ABI (ORG/LDS/JSR main/halt) + cuerpo
    lineas = []
    lineas.append(f"\tORG ${cfg.org:04X}")
    lineas.append("start:")
    lineas.append(f"\tLDS #${cfg.stack_init:04X}")
    lineas.append("\tJSR main")
    lineas.append("halt:")
    lineas.append("\tRTS" if cfg.halt == "rts" else "\tSWI")
    lineas.append("main:")
    lineas.extend(instrs)
    lineas.append("\tEND")
    return AsmProgram(lineas=lineas)
