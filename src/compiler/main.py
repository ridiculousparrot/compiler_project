from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpretador



def main():
    codigo = 'print 1 + 2;'

    # Lexer
    lexer = Lexer(codigo)
    tokens = lexer.scan_tokens()

    # Parser
    parser = Parser(tokens)
    statements = parser.parse()

    # Interpretador
    interpretador = Interpretador()
    interpretador.interpretar(statements)


if __name__ == "__main__":
    main()
