class ErrorCompilacion(Exception):
    pass


class ErrorFrontend(ErrorCompilacion):
    pass


class ErrorIR(ErrorCompilacion):
    pass


class ErrorBackend(ErrorCompilacion):
    pass
