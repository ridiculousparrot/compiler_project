import types
from xmlrpc.client import Binary
from compiler_project.src.lexer.lexer import TokenType
from compiler_project.src.utils.errors import parserError
from compiler_project.src.parser.ast import Expr

class Parser:   
    def __init__(self, tokens):
        # Inicializa o Parser com a lista de tokens.
        # Parâmetros:
        # - tokens: lista de tokens produzidos pelo lexer.

        self.tokens = tokens
        self.current = 0    

    #Istancia o tokens e o valor por onde deve comecar a separacao incial, logo = 0

    def espiar(self):
        # Retorna o token atual sem avançar o cursor.
        # Retorna o token na posição `self.current`.

        return self.tokens[self.current]

    #retorna valores dos tokens instanciados, caso nao tenha valor
    
    def anterior(self):
        # Retorna o token imediatamente anterior ao atual.
        # Útil após `advance()` para recuperar o token recém-lido.

        return self.tokens[self.current -1]

    #retorna o valor antigo do token, caso precise, logo o valor do token atual recebe -1
    
    def fim(self):
        # Retorna True se o token atual for o token de EOF.
        # Indica término da sequência de tokens.

        return self.espiar().type == TokenType.EOF

    #marca o fim da tokenizacao, onde a quandidade de tokens objtidos e igual ao valor alocado.
    
    def avancar(self):
        # Avança para o próximo token e retorna o token anterior.
        # Se não chegar ao fim, incrementa `self.current`.

        if not self.fim():
            self.current += 1

    #ao terminar a leitura e separacao de um token gerado ao lexer, parte para a proxima leitura

        return self.anterior()
    
    def verificar_fim(self, *types):
        # Verifica se o token atual é do tipo `type_`.
        # Retorna False se estivermos no fim dos tokens.

        if self.fim():
            return False

    #verifica se a leitura dos tokens vundo do lexer terminaram
        
        return self.espiar().type in types
    
    def parser_math(self, *types):
       # Tenta parsear uma expressão matemática.
       # Implementação atual: percorre a coleção `types` em busca de um tipo
       # correspondente e, se encontrado, avança e retorna True.

       for type_ in types:
           if self.verificar_fim(type_):
               self.avancar()
               return True
           return False
    
    def costume(self, type_, message):
        # Consume um token do tipo esperado ou lança `parserError`.
        # Parâmetros:
        # - type_: tipo de token esperado.
        # - message: mensagem de erro caso o token não seja o esperado.

        if self.verificar_fim(type_):
            return self.avancar()
        
        raise parserError(self.espiar().line, message)
    
    def parser_gram(self):
        # Parseia a gramática de nível superior e retorna uma lista de statements.
        # Implementação atual: esqueleto que recolhe chamadas a `parser_math`.

        statement = []

        while not self.fim():
            statement.append(self.parser_math)

        return statement

    def expressao(self):  
        # Ponto de entrada para parsear uma expressão; delega para `parser_math`.

        return self.parser_math() 

    def declaracao_variavel(self):
        # Parseia uma declaração de variável.
        # Fluxo esperado: identifica o nome, o operador de atribuição, a expressão inicializadora
        # e o separador (`;`). A implementação atual retorna uma chamada recursiva,
        # portanto é um placeholder que precisa ser ajustado para construir o nó AST.

        name = self.costume(TokenType.IDENTIFIER, "Esperado um identificador após a palavra reservada 'var'.")
        self.costume(TokenType.EQUAL, "Esperado '=' após o identificador.")

        inicializador = self.expressao()   
        self.costume(TokenType.SEPARATOR, "Esperado ';' após a declaração da variável.")

        return Var(name, inicializador)
  
    def termo(self):
        # Parseia um termo numa expressão combinando fatores com operadores.
        # Exemplo: lê um fator, então enquanto encontrar `+` ou `-` combina em uma
        # estrutura `Binary`.

        expr = self.factor()

        while self.verificar_fim(TokenType.PLUS, TokenType.MINUS): 
            operator = self.anterior()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr


    #definimos agora as regras do parse dentro da atual rotatividade do sistema
    #define o estado statement como uma lista-array
    #intancia a funcao fim ja comentarta acima
    def parse(self):
        statements = []
        while not self.fim():
            statements.append(self.declaracao())
            #chama a funcao statment e retorna o valor que ele pega
            #adiciona em uma lista chamada statement, na qual declaramos no inicio da funcao
        return statements
    #retorna a lista statement

    def estado(self):
     #chama a funcao estado que faz uma validacao
     #se a validacao chamando a funcao math() tiver o valor retornado da funcao espiar
     #retornar o valor do statement
        if self.verificar_fim(TokenType.PRINT):
            return self.mostrar_estado()

        return self.expressao_estado()
    #retorna toda a construcao da lista statement

    def mostrar_estado(self):
        #valor da expresssao e chamado
        #funcao costume retornando um erro de parser
        value = self.expressao()
        self.costume(
        TokenType.SEPARATOR,
        "Esperado ';' depois desse valor.")
        return print(value) 


    def expressoes_estado(self):
        #expressao tambem recebe um valor e retorna um erro de parser vindo do costume
        Expr = self.expressao()
        self.costume(TokenType.SEPARATOR, "Esperado ';' depois desse valor")
        return print(Expr)


        
#temos aqui a funcao cuja retorna a declaracao da variavel
    def declaracao(self):
        if self.verificar_fim(TokenType.VAR):
            return self.declaracao_variavel()

        if self.verificar_fim(TokenType.SE):
            return self.declaracao_se()
        return self.estado()

    def primary(self):
        if self.parser_math(TokenType.IDENTIFIER):
            return Variable(self.anterior())
        
#declaracao do SE, validando a sintaxe com os erros de esperado
#retorna os valores de entao, senao e condicao

    def delcaracao_se(self):
        self.costume(TokenType.LEFT_PAREN, "Esperado '(' depois de 'SE' ).")

        condition = self.expressao()

        self.costume(TokenType.RIGHT_PAREN, "Esperado ')' depois da 'condicao'.")

        entao = self.declaracao()

        senao = None

        if self.parser_math(TokenType.SENAO):
            senao = self.declaracao()

            return Se(
            condition,
            entao,
            senao
        )
