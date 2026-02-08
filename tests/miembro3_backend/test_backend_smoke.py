import pytest
from hc11cc.config import Config
from hc11cc.backend.hc11.program import envolver_programa
from hc11cc.backend.hc11.emit import emit_asm


@pytest.mark.backend
def test_backend_smoke():
    cfg = Config()
    prog = envolver_programa([], cfg)
    asm = emit_asm(prog)
    assert "ORG" in asm
    assert "LDS" in asm
    assert "JSR main" in asm
