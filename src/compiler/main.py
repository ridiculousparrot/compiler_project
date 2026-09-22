from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import Interpretador

#PARA TESTAR -------------
##// Declaração simples
##var x = 10;

##// Expressão com operadores
##var soma = 5 + 3 * 2;

##// String
##var nome = "Pedro"

##// Condicional (SE / SENAO)
##se (x > 5) {
##    print(x);
##} senao {
##    print(0);
##}

##// Laço ENQUANTO
##enquanto (x > 0) {
##    x = x - 1;
##}

##// Laço FACA (do-while)
##faca {
##x = x + 1
##} enquanto (x < 10);

##// Função e retorno
##funcao soma(a, b) {
##   retorno a + b;
##}

##// Switch / case (TROCAR / QUEBRAR)
##trocar (x) {
##    caso 1:
##        print("um");
##        quebrar;
##    caso 2:
 ##       print("dois");
 ##       quebrar;
##}

##// Comparações e diferente
##se (x != 10) {
##    print("diferente");
##}


##//faca enquanto e enquanto 

#var x = 0;
#faca {
  #  print("Executando");
 #   x = x + 1;
#} enquanto (x < 10);
#

"""
x = 10;

se (x > 5) {
    print(x);
} entao {
    print(0);
} senao {
    print(-1);
}
"""


def main():
    codigo = """
funcao soma(a, b) {
    retorno a + b;
}

funcao teste() {
    var x = 10;
    var somaResultado = soma(5, 3 * 2);
    var nome = "Pedro";

    se (x < 5) {
        print(x);
    } senao {
        print(0);
    }

    enquanto (x > 0) {
        x = x - 1;
    }

    faca {
        x = x + 1;
    } enquanto (x < 10);

    trocar (x) {
        caso 1:
            print("um");
            quebrar;
        caso 2:
            print("dois");
            quebrar;
    }

    se (x != 10) {
        print("diferente");
    }

    var contador = 0;

    faca {
        contador = contador + 1;
    } enquanto (contador < 1);

    retorno 1;
}

var resultado = teste();
print(resultado);
    """

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

