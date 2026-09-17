from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import Interpretador

#PARA TESTAR -------------
##// Declaração simples
##var x = 10

##// Expressão com operadores
##var soma = 5 + 3 * 2

##// String
##var nome = "Pedro"

##// Condicional (SE / SENAO)
##se (x > 5) {
##    print(x)
##} senao {
##    print(0)
##}

##// Laço ENQUANTO
##enquanto (x > 0) {
##    x = x - 1
##}

##// Laço FACA (do-while)
##faca {
##x = x + 1
##} enquanto (x < 10)

##// Função e retorno
##funcao soma(a, b) {
##   retorno a + b
##}

##// Switch / case (TROCAR / QUEBRAR)
##trocar (x) {
##    caso 1:
##        print("um")
##        quebrar
##    caso 2:
 ##       print("dois")
 ##       quebrar
##}

##// Comparações e diferente
##se (x != 10) {
##    print("diferente")
##}

def main():
    codigo = 'var x = 10;' \
    'se (x > 5) {' \
    ' print(x);' \
    '} senao {' \
    'print(0);' \
    '}'
    # Lexer
    lexer = Lexer(codigo)
    tokens = lexer.scanear_tokens()

    # Parser
    parser = Parser(tokens)
    statements = parser.parse()

    # Interpretador
    interpretador = Interpretador()
    for stmt in statements:
        resultado = interpretador.executar(stmt)
    if resultado is not None:
        print(interpretador.stringify(resultado))

if __name__ == "__main__":
    main()

