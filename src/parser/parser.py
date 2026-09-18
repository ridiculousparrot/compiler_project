import types
from src.lexer.lexer import TokenType
from src.utils.errors import parserError
from src.parser.ast import (
    Bloco,
    Faca_enquanto,
    Se,
    Var,
    Variable,
    Expr,
    funcao,
    Enquanto,
    Declaracao,
    Binary,
    Unary,
    Print,
    Literal,
    Grouping,
    ExpressaoStatement,
    retorno,
    Atribuicao,
    chamar
)



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


    def declaracao_variavel(self):
        # Parseia uma declaração de variável.
        # Fluxo esperado: identifica o nome, o operador de atribuição, a expressão inicializadora
        # portanto é um placeholder que precisa ser ajustado para construir o nó AST.
        self.costume(TokenType.VARIAVEL, "Esperado uma variavel()")
        name = self.costume(TokenType.IDENTIFICADOR, "Esperado um identificador após a palavra reservada 'var'.")
        self.costume(TokenType.IGUAL_OUTRO, "Esperado '=' após o identificador.")

        initializer = self.expressao()   
        self.costume(TokenType.PONTO_VIRGULA, "Esperado ';' após a declaração da variável.")
        return Var(name, initializer)

# Parseia um termo numa expressão combinando fatores com operadores.
        # Exemplo: lê um fator, então enquanto encontrar `*` ou `/` combina em uma
        # estrutura `Binary`.

    def unario(self):
        ##expressoes unarias trabaham apenas com uma expressao.
                # Parseia um termo numa expressão combinando fatores com operadores.
                # Exemplo: lê um fator, então enquanto encontrar `+` ou `-` combina em uma
                # estrutura `unario`.
        if self.verificar_fim(TokenType.MAIS, TokenType.MENOS):
                    
            operador = self.avancar()
            direita = self.chamada()
        
            return self.chamada()
                

        return self.chamada()
        ###unario
  # ↓
#encontrou "-"?
   #↓ sim
#operador = "-"
  # ↓
#lê outra expressão unária
#   ↓
#Unary("-", expressão)

  



    def expressao(self):  
        # Ponto de entrada para parsear uma expressão; delega para `parser_math`.
        return self.atribuicao()

    def atribuicao(self):
        expr = self.igualdade()

        if self.verificar_fim(TokenType.IGUAL_OUTRO):
            igual = self.avancar()
            valor = self.atribuicao()
            if isinstance(expr, Variable):
                return Atribuicao(expr.name, valor)

            raise parserError(igual.line, "Atribuicao pode ser feitas em variaveis declaradas")

        return expr  

    def igualdade(self):
        expr = self.comparacao()
        while self.verificar_fim(TokenType.IGUAL_IGUAL, TokenType.DIFERENTE):
            operador = self.avancar()
            direita = self.comparacao()
            expr = Binary(expr, operador, direita)
        return expr

    def comparacao(self):
        expr = self.adicao()
        while self.verificar_fim(TokenType.MAIOR_IGUAL, 
                                 TokenType.MENOR_IGUAL, 
                                 TokenType.MAIOR, 
                                 TokenType.MENOR):
           operador = self.avancar()
           direita = self.adicao()
           expr = Binary(expr, operador, direita)
        return expr 
    
    def adicao(self):
        expr = self.termo()
        while self.verificar_fim(TokenType.MAIS, TokenType.MENOS):
            operador = self.avancar()
            direita = self.termo()
            expr = Binary(expr, operador, direita)
        return expr


    def fator(self):
        if self.verificar_fim(TokenType.NUMERO):
            token = self.avancar()
            return Literal(token.literal)

        if self.verificar_fim(TokenType.STRING):
            token = self.avancar()
            return Literal(token.literal)

        if self.verificar_fim(TokenType.IDENTIFICADOR):
            return Variable(self.avancar())

        if self.verificar_fim(TokenType.PARENTESES_ESQUERDO, "Esperado '(' apos a expressao :("):
            self.avancar()
            expr = self.expressao()
            self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')' após a expressão.")
            return Grouping(expr)
        raise parserError(self.espiar().line, "Esperado uma expressão.")


  
    def termo(self):
        # Parseia um termo numa expressão combinando fatores com operadores.
        # Exemplo: lê um fator, então enquanto encontrar `+` ou `-` combina em uma
        # estrutura `Binary`.

        expr = self.unario()

        while self.verificar_fim(TokenType.MULTIPLICACAO, TokenType.BARRA):
            operador = self.avancar()
            direita = self.unario()

            expr = Binary(expr,operador,direita)

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
        #valor da expressao e chamado
        #funcao costume retornando um erro de parser
       self.costume(TokenType.PRINT, "Esperado 'print'.")
       value = self.expressao()
       self.costume(TokenType.PONTO_VIRGULA, "Eesperado ';'")
       return Print(value)


    def expressao_estado(self):
        #expressao tambem recebe um valor e retorna um erro de parser vindo do costume
        expr = self.expressao()
        self.costume(TokenType.PONTO_VIRGULA, "Esperado ';' depois da expressao.")
        return ExpressaoStatement(expr)


        
#temos aqui a funcao cuja retorna a declaracao da variavel
#Necessario realizar a funcao de verificar fim para todos os tipos de tokens que podem ser declarados, como variavel, se, senao, enquanto e faca enquanto

    def declaracao(self):
        if self.verificar_fim(TokenType.VARIAVEL):
            return self.declaracao_variavel()
        if self.verificar_fim(TokenType.SE):
            return self.declaracao_se()

        if self.verificar_fim(TokenType.ENQUANTO):
            return self.declaracao_enquanto()

        if self.verificar_fim(TokenType.RETORNO):
            return self.declaracao_retorno()

        if self.verificar_fim(TokenType.FACA):
            return self.declaracao_faca_enquanto()
        if self.verificar_fim(TokenType.CHAVES_ESQUERDO):
            return self.bloco()
        if self.verificar_fim(TokenType.FUNCAO):
            return self.declaracao_funcao()
        return self.estado()


    def primary(self):
        if self.parser_math(TokenType.IDENTIFICADOR):
            return Variable(self.anterior())
        
        #regra de atribuicao de valor em uma variavel, caso o token seja do tipo IDENTIFIER, ele retorna a variavel com o valor do token anterior
    def atribuicao_varivavel(self):
        #chama a funcao expressao para pegar o valor da expressao e verificar os tokens
        Expr = self.expressao()
#se o token for do tipo equal, ele retorna o valor do token anterior e o valor da expressao, se for variavel, ele retorna o nome e o valor, 
#caso no seja valor da variavel, ele retorna um erro de parser, informando que a atribuicao de valor pode ser feita apenas em variaveis declaradas
        if self.parser_math(TokenType.IGUAL_OUTRO):
            equals = self.anterior()
            value = self.atribuicao_variavel()
# a funcao isinstance verifica se o objeto Expr é uma instância da classe Variable, ou seja, se Expr representa uma variável. Se for verdadeiro, 
# ele cria e retorna um objeto Var com o nome da variável, o valor atribuído e o token de igualdade. Caso contrário, 
# ele levanta um erro de parser informando que a atribuição de valor só pode ser feita em variáveis declaradas.
            if isinstance(Expr, Variable):
                return Var(Expr.name, value, equals)

            raise parserError(equals.line, "atribuicao de valor pode ser feita apenas em variavies declaradas")
#retorna toda expressao 
        return Expr

#funcao que parseia um bloco de codigo
    def bloco(self):
        self.costume(TokenType.CHAVES_ESQUERDO, "Esperado '{'.")
        statements = []
        while not self.verificar_fim(TokenType.CHAVES_DIREITO) and not self.fim():
            statements.append(self.declaracao())
        self.costume(TokenType.CHAVES_DIREITO, "Esperado '}' após o bloco.")
        return Bloco(statements)

#declaracao do SE, validando a sintaxe com os erros de esperado
#retorna os valores de entao, senao e condicao

    def declaracao_se(self):
        self.costume(TokenType.SE, "Esperado 'se'. ")
        self.costume(TokenType.PARENTESES_ESQUERDO, "Esperado '(' depois de 'SE' ).")

        condition = self.expressao()

        self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')' depois da 'condicao'.")

        entao = self.declaracao()

        senao = None

        if self.parser_math(TokenType.SENAO):
            senao = self.declaracao()

        return Se(
            condition,
            entao,
            senao
        )
#declaracao do ENQUANTO, validando a sintaxe com os erros de esperado

    def declaracao_enquanto(self):
        self.costume(TokenType.ENQUANTO, "Esperado 'ENQUANTO'.")

        self.costume(TokenType.PARENTESES_ESQUERDO, "Esperado '(' depois de 'ENQUANTO'.")

        condition = self.expressao()

        self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')' depois da 'CONDICAO'.")

        enquanto = self.declaracao()

        return Enquanto(
                condition,
                enquanto
            )
    
#declaracao do FACA ENQUANTO, agora eles precisam existir ao mesmo tempo 
    def declaracao_faca_enquanto(self):
        self.costume(TokenType.FACA, "Esperado FAC A depois de 'FACA'.")

        faca_enquanto = self.declaracao()


        self.costume(TokenType.ENQUANTO, "Esperado ENQUANTO depois de  FACA.")


        self.costume(TokenType.PARENTESES_ESQUERDO, "Esperado '(' depois de 'ENQUANTO'.")

        condition = self.expressao()

        self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')' depois da 'CONDICAO'.")


        return Faca_enquanto(
                faca_enquanto,
                condition
        )


### AS CHAMADAS PERMITEM QUE FAZERMOS AS FUNCOES DE UMA CHAMADA PARA ABERTURA DE UMA FUNCAO (PARAMETRO + PARAMETRO B)
### JOGA EM LACO CASO ACHA O TOKEN DE PARENTESES
## RETORNA RESULTADO DA EXPRESSAO VINDA DO FATOR
# FINALIZAR CHAMADA DEFININDO ARGUMENTOS COMO UMA LISTA VAZIA, SE NAO TIVER TOKEN DE PARENTESES DIRETO, DA ERRO, MAS SE TIVER
#FACILITA A LEITURA DO TOKEN ',' E DENTRO DELE SE ESPERA A DECLARACAO DA EXPRESSAO DENTRO DOS PARENTESESm RETORNANDO OS ARGUMENTOS, A CHAMADA 
#E OS PARAMETROS
    def chamada(self):
        expr = self.fator()

        while True:
            if self.verificar_fim(TokenType.PARENTESES_ESQUERDO):
                self.avancar()
                expr = self.finalizar_chamada(expr)
            else:
                break

        return expr

    def finalizar_chamada(self, calle):
        argumentos = [
        ]

        if not self.verificar_fim(TokenType.PARENTESES_DIREITO):
            argumentos.append(self.expressao())
            while self.parser_math(TokenType.VIRGULA):
                argumentos.append(self.expressao())

        paren = self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')'.")
        return chamar(calle, paren, argumentos)





















#relativamente, essa foi a funcao mais complexa de se fazer,
#a funcao declaracao funcao, vai trabalhar com os devidos tokens, funcao, parametro identificador, parenteses esquerdo e direito, 
# chaves esquerdo e direito, e vai retornar a funcao com o nome, parametros e corpo da funcao
    def declaracao_funcao(self):

        self.costume(TokenType.FUNCAO, "Esperado 'FUNCAO',")

        name = self.costume(TokenType.IDENTIFICADOR, "Esperado um identificador depois de 'funcao'.")

        self.costume(TokenType.PARENTESES_ESQUERDO, "Esperado '(' depois de 'FUNCAO'.")

#parametros nao sao obrigatorios, caso nao seja declarado, a lista de parametros sera vazia
        parametros = []

#mas no caso se for declarado, ele vai verificar 
# se o token e diferente de parenteses 
# direito, caso seja diferente, ele vai adicionar o parametro na lista de parametros
        if not self.verificar_fim(TokenType.PARENTESES_DIREITO):
            parametros.append(
            self.costume(
                TokenType.IDENTIFICADOR,
                "esperado nome do parametro"
            )
        )
#virgula para separar os parametros, caso tenha mais de um, e vai adicionar na lista de parametros soma(a, b) exemplo
        while self.parser_math(TokenType.VIRGULA):
            parametros.append(
                self.costume(
                    TokenType.IDENTIFICADOR,
                    "esperado nome do parametro."
                )
            )
#chama tokens da funcao, parenteses e chaves
        self.costume(TokenType.PARENTESES_DIREITO, "Esperado ')' depois de 'FUNCAO'.")

        self.costume(TokenType.CHAVES_ESQUERDO, "Esperado '{' depois de 'FUNCAO'.")
#o corpo de uma funcao nao necessariamente precisa ter um valor, caso tenha recebera uma lista vazia
        corpo = []
#enquanto nao for o token de chaves direito, ele vai adicionar o corpo da funcao na lista de corpo

        while not self.verificar_fim(TokenType.CHAVES_DIREITO) and not self.fim():
             corpo.append(self.declaracao())
#token de fechar token
        self.costume(TokenType.CHAVES_DIREITO, "Esperado '}' depois de 'FUNCAO'.")
#retorna a funcao com o nome, parametros e corpo da funcao
        return funcao(
            body=Bloco(corpo),
            name = name,
            parametros = parametros)

    def declaracao_retorno(self):
        self.costume(TokenType.RETORNO, "Esperado 'retorno'.")
        value = None
        if not self.verificar_fim(TokenType.PONTO_VIRGULA):
            value = self.expressao()
            self.costume(TokenType.PONTO_VIRGULA, "Esperado ';' depois da expressao.")
        return retorno(value)
    