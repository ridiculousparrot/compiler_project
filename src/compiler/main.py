from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import Interpretador

# PARA TESTAR -------------
##// Declaração simples
##var x = 10;

##// Expressão com operadores
##var soma = 5 + 3 * 2;

##// String
##var nome = "Pedro"

##// Condicional (SE / SENAO)
##se (x > 5) {
##    mostrar(x);
##} senao {
##    mostrar(0);
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
##        mostrar("um");
##        quebrar;
##    caso 2:
##       mostrar("dois");
##       quebrar;
##}

##// Comparações e diferente
##se (x != 10) {
##    mostrar("diferente");
##}


##//faca enquanto e enquanto

# var x = 0;
# faca {
#  mostrar("Executando");
#   x = x + 1;
# } enquanto (x < 10);
#

"""
x = 10;

enquanto (x <10) {
mostrar ("FUNCIONANDO");
x = x + 1;


####


x = 10, 9, 8 7;
mostrar(x);
}

"""


def main():
    codigo = """

funcao somar(a, b) {
    retorno a + b;
}

funcao maior(a, b) {
    se (a > b) {
        retorno a;
    } senao {
        retorno b;
    }
}

principal() {

    var numeros = [10, 20, 30, 40, 50];

    mostrar("=== LUDUS ===");

    mostrar("Vetor criado:");

    mostrar(numeros);

    var x = 10;

    se (x > 5) {
        mostrar("x e maior que 5");
    } senao {
        mostrar("x nao e maior que 5");
    }

    enquanto (x > 5) {
        x = x - 1;
    }

    mostrar("Valor de x:");

    mostrar(x);

    var resultado = somar(7, 8);

    mostrar("Resultado da soma:");

    mostrar(resultado);

    var maior_valor = maior(25, 42);

    mostrar("Maior valor:");

    mostrar(maior_valor);

    faca {
        x = x + 1;
    } enquanto (x < 10);

    mostrar("Valor final de x:");

    mostrar(x);

}
    """

    # Lexer
    lexer = Lexer(codigo)
    tokens = lexer.scanear_tokens()

    # Parser
    parser = Parser(tokens)
    statements = parser.parse()

    # Interpretador
    interpretador = Interpretador()
    interpretador.analisar_arvore_sintatica(statements)
    for stmt in statements:
        resultado = interpretador.executar(stmt)
    if resultado is not None:
        print(interpretador.stringify(resultado))


if __name__ == "__main__":
    main()
