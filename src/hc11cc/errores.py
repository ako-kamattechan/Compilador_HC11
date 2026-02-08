from dataclasses import dataclass
from typing import Optional

# Evitar import circular: no importar Span type checking aquí si no es estrictamente necesario en runtime,
# pero para tipeo lo ideal es `from typing import TYPE_CHECKING`
if False:  # TYPE_CHECKING hack
    from hc11cc.frontend.tokens import Span


class ErrorCompilacion(Exception):
    pass


class ErrorFrontend(ErrorCompilacion):
    def __init__(self, message: str, span: Optional["Span"] = None):
        super().__init__(message)
        self.message = message
        self.span = span

    def __str__(self):
        if self.span:
            return f"{self.message} at {self.span}"
        return self.message


class ErrorIR(ErrorCompilacion):
    pass


class ErrorBackend(ErrorCompilacion):
    pass
