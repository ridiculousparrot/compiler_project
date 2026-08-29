
class parserError(Exception):

    def __init__(self, line, message):
        self.line = line
        self.message = message
        super().__init__(f"Erro de sintaxe na linha {line}: {message}")

class runtimeError(Exception):

    def __init__(self, line, message):
        self.line = line
        self.message = message
        super().__init__(f"Erro de execução na linha {line}: {message}")
