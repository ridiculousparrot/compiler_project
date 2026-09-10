from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import Interpretador



def main():
    codigo = 'print 1 + 2;'

    # Lexer
    lexer = Lexer(codigo)
    tokens = lexer.scanear_tokens()

    # Parser
    parser = Parser(tokens)
    statements = parser.parse()

    # Interpretador
    interpretador = Interpretador()
    interpretador.visitarExpressaoStmt


if __name__ == "__main__":
    main()
