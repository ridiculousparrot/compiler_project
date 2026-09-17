from src.lexer.lexer import TokenType
from src.parser.ast import Literal, Grouping, Unary, Binary, Print, Var, Faca_enquanto, Se, Enquanto, Bloco, retorno, ExpressaoStatement, Variable, Atribuicao
class Interpretador:

    def __init__(self):
        #define o ambiente da linguagem e guarda espaco para declaracoes de variaveis
        self.ambiente = {}

    #cria a classse interpretador, que é responsável por avaliar e executar as expressões da linguagem.

# avaliar, visitarExpressaoLiteral, visitarExpressaoAgrupada, visitarExpressaoUnaria, seVerdadeiro, 
# visitarExpressaoBinaria servirao para avaliar e executar as expressões da linguagem, 
# retornando os resultados correspondentes.

    def avaliar(self, expr):
        if isinstance(expr, Literal):
            return self.visitarExpressaoLiteral(expr)
        if isinstance(expr, Grouping):
            return self.visitarExpressaoAgrupada(expr)
        if isinstance(expr, Unary):
            return self.visitarExpressaoUnaria(expr)
        if isinstance(expr, Binary):
            return self.visitarExpressaoBinaria(expr)
        if isinstance(expr, Var):
            return self.visitar_variavel(expr)
        if isinstance(expr, Variable):
            return self.visitarVariableExpr(expr)
        if isinstance(expr, Atribuicao):
            return self.visitar_atribuicao(expr)

        raise Exception(f"Tipo de expressão desconhecido: {type(expr)}")

    # faz com que a expressão aceite o interpretador, chamando o método apropriado para avaliar o tipo específico de expressão.

    def visitarExpressaoLiteral(self, expr):
        return expr.value

    #faz com que a expressão literal retorne seu valor diretamente, sem necessidade de avaliação adicional.
    
    def visitarExpressaoAgrupada(self, expr):
        return self.avaliar(expr.expression)
    
    #faz com que a expressão agrupada seja avaliada chamando o método avaliar na expressão interna, permitindo que a precedência seja respeitada.
    
    def visitarExpressaoUnaria(self, expr):
        direita = self.avaliar(expr.right)
    #faz com que a expressão unária seja avaliada chamando o método avaliar no operando direito, permitindo que o operador unário seja aplicado ao valor resultante.

        match expr.operator.type:

            case TokenType.MENOS:
                return -direita

            case TokenType.NEGACAO:
                return not self.seVerdadeiro(direita)

        return None
    # essa função avalia expressões unárias, aplicando o operador unário apropriado ao valor do operando direito e retornando o resultado.

    def seVerdadeiro(self, value):
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return True
    
    # se for None, retorna False; se for um booleano, retorna seu valor; caso contrário, considera o valor como verdadeiro.

    def visitarExpressaoBinaria(self, expr):
        esquerda = self.avaliar(expr.left)
        direita = self.avaliar(expr.right)

    #visita a expressão binária, avaliando os operandos esquerdo e direito chamando o método avaliar em cada um deles, permitindo que a operação binária seja aplicada aos valores resultantes.
        
        match expr.operator.type:
            
            case TokenType.MENOS:
                return esquerda - direita

            case TokenType.MAIS:
                return esquerda + direita       

            case TokenType.BARRA:
                return esquerda / direita

            case TokenType.MULTIPLICACAO:
                return esquerda * direita

            case TokenType.MAIOR:
                return esquerda > direita

            case TokenType.MAIOR_IGUAL:
                return esquerda >= direita

            case TokenType.MENOR:
                return esquerda < direita

            case TokenType.MENOR_IGUAL:
                return esquerda <= direita

            case TokenType.IGUAL_OUTRO:
                return esquerda != direita

            case TokenType.IGUAL_IGUAL:
                return esquerda == direita

        return None

    #aqui comeca a forma como a linguagem vai interpretar as expressoes binarias, aplicando o operador binário apropriado aos valores dos operandos esquerdo e direito e retornando o resultado da operação.

#funcao responsavel por executar os statements, chamando o metodo accept para que o statement aceite o interpretador e execute a ação correspondente.
    def executar(self, stmt):
        if isinstance(stmt, Print):
            return self.visitarPrintStmt(stmt)
        if isinstance(stmt, Se):
            return self.visitar_se(stmt)
        if isinstance(stmt, Enquanto):
            return self.visitar_enquanto(stmt)
        if isinstance(stmt, retorno):
            return self.visitar_retorno(stmt)
        if isinstance(stmt, Faca_enquanto):
            return self.visitar_faca_enquanto(stmt)
        if isinstance(stmt, ExpressaoStatement):
            return self.visitarExpressaoStmt(stmt)
        if isinstance(stmt, Bloco):
            return self.visitar_bloco(stmt)
        raise Exception(f"Tipo de statement desconhecido: {type(stmt)}")
    
# visita a expressão de print, avaliando a expressão e imprimindo o resultado na saída padrão.
    def visitarExpressaoStmt(self,stmt):
        self.avaliar(stmt.expression)
        return None

#define funcao de definir uma variavel 

    def definir_variavel(self, nome, valor):
        self.ambiente[nome] = valor
##funcao que busca os valores da variavel ou o nome atribuida a valor x, logo ele retorna o nome depois
#de uma validacao de nome nas variaveis.
    def buscar_variavel(self, name_token):
        nome = name_token.lexeme
        if nome in self.ambiente:
            return self.ambiente[nome]
        raise Exception(f"Variavel nao definida {nome} na linha {name_token.line}")
##Visitar variavel nessecario para ler o que e variabel, a atribuicao do seu nome com if, chamando a expressao expr, variavel nao perternce ao grupo de statements
#se nao estiver no ambiente retorna exception para que nao seja declarada
#retorna o ambimente com o nome dela caso nao cair na chamada condicional


##A atribuicao da expressao, valor chama a expressao do valor que existe e retorna ao ambiente criado
    def visitar_atribuicao(self, expr):
        value = self.avaliar(expr.value)
        self.ambiente[expr.name.lexeme] = value
        return value
    
#visita a  o print statement, avaliando a expressão e imprimindo o resultado na saída padrão.
    def visitarPrintStmt(self, stmt):
        value = self.avaliar(stmt.expression)
        print(self.stringify(value))
        return None

#a funcao interpretar_funcao recebe uma lista de statements e 
# executa cada um deles chamando o método executar, permitindo que a função seja interpretada e suas ações sejam realizadas.
    def interpretar_funcao(self, stmt):
         for statement in statement:
            self.executar(statement)

    #verifica se o valor e nulo, caso sim, retorna nulo, se for booleano, retorna o valor, caso contrario, considera o valor como verdadeiro
    def stringify(self, value):
        if value is None:
            return "nulo"
#
        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, float):
            texto = str(value)
            # remove o ".0" de números inteiros (ex: 3.0 -> "3")
            if texto.endswith(".0"):
                texto = texto[:-2]
            return texto

        return str(value)

    #converte o valor resultante da avaliação em uma string, seguindo as
    #convenções da linguagem: None vira "nil", booleanos ficam em
    #minúsculo ("true"/"false") e números com .0 perdem a casa decimal.


#visitar declaracao variavel, o valor dela se inicia como valor nula, caso o valor do inicializador seja diferente de nulo
#istancia a funcao avaliar, que vai avaliar o valor do inicializador(arvore sintatica) e retornar o valor da variavel
    def visitar_declaracao_variavel(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.avaliar(stmt.initializer)
            self.definir_variavel(stmt.name.lexeme, value)
        return value

#funcao de visitar variavel
    def visitarVariableExpr(self, expr):
        return self.buscar_variavel(expr.name)
#visitar a condicao se, se existe a condicao dentro do statement  
# visita se a condicao for verdadeira
    def visitar_se(self, stmt):
        condition = self.avaliar(stmt.condition)
        if self.seVerdadeiro(condition):
            self.executar(stmt.entao)

        elif stmt.senao is not None:
            self.executar(stmt.senao)
#visitar a condicao enquanto, se a condicao for verdadeira, executa o corpo do while, e repete o processo até que a condicao seja falsa

    def visitar_enquanto(self, stmt):
        while self.seVerdadeiro(self.avaliar(stmt.condition)):
            self.executar(stmt.body)

#visitar a condicao faca enquanto, quando executa o circulo do while, verrifica a condicao, se for verdadeira repetete o processo, caso falsa, encerra o loop
    def visitar_faca_enquanto(self, stmt):
        while True:
            self.executar(stmt.body)
            if not self.seVerdadeiro(self.avaliar(stmt.condition)):
                break 

    def visitar_funcao(self, stmt):
        #aqui a funcao vai retornar o valor da funcao, que pode ser None caso a expressao digitada nao tenha valor
        return stmt

#regra de retur, define valor de retorno = nulo, se o valor do statemnt nao for nulo, ele avalia noamente o valor da statement, e retorna 
# o valor da expressao digitada, caso nao tenha valor, retorna nulo
    def visitar_retorno(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.avaliar(stmt.value)
        return value

##Visitar variavel nessecario para ler o que e variabel, a atribuicao do seu nome com if, chamando a expressao expr, variavel nao perternce ao grupo de statements
#se nao estiver no ambiente retorna exception para que nao seja declarada
#retorna o ambimente com o nome dela caso nao cair na chamada condicional


    def visitar_bloco(self, stmt):
        resultado = None
        for statement in stmt.statements:
            resultado = self.executar(statement)
        return resultado 