import pytest


@pytest.fixture
def ejemplo_minimo():
    # Por ahora no parsea realmente; sirve para smoke tests.
    return "fn main() -> u8 { return 7; }"
