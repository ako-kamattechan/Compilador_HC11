from dataclasses import dataclass


@dataclass
class Config:
    emitir_ir: bool = False
    debug: bool = False
    org: int = 0x0100
    stack_init: int = 0x01FF
    halt: str = "rts"  # "rts" o "swi"
