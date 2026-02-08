import pytest
from hc11cc import compilar, Config


@pytest.mark.integracion
def test_pipeline_smoke(ejemplo_minimo):
    cfg = Config(emitir_ir=False)
    asm = compilar(ejemplo_minimo, cfg)
    assert "main:" in asm
