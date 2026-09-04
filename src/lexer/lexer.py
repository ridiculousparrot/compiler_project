from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Palavra reservada para declaração de variáveis.
    # Exemplo: var x = 10;
    VARIAVEL = auto()

    # Nome dado pelo programador para variáveis,
    # funções, classes, etc.
    # Exemplos: x, contador, soma, minhaFuncao
    IDENTIFICADOR = auto()

    # Valores numéricos.
    # Exemplos: 10, 3.14, 42
    NUMERO = auto()

    # Cadeias de caracteres delimitadas por aspas.
    # Exemplos: "Olá Mundo", "Pedro"
    STRING = auto()

    # Operadores da linguagem.
    # Exemplos: +, -, *, /, =, ==, !=, <, >
    OPERADORES = auto()

    # Símbolos que organizam a sintaxe.
    # Exemplos: ; , ( ) { } [ ]
    SEPARADORES = auto()

    # Marca o final do arquivo ou entrada.
    # Facilita o parser saber quando encerrar a análise.
    EOF = auto()

    # aqui onde sera definido os tokens, como palavras reservadas, operadores, etc.

    SE = auto()

    #define token da paralvra reservada para se  (if)

    SENAO = auto()

    #define token da palavra senao (if)

    FACA = auto()

    #define token para faca (do)

    ENQUANTO = auto()

    #define token para enquanto enquanto (while)

    #define token para funcao (function)
    FUNCAO = auto()

    #define token para return (return)
    RETORNO = auto()


    #define token do switrch case (case), ou seja, trocar
    TROCAR = auto()

    #define token do break, ou seja, quebrar o fluxo de execucao do switch case
    QUEBRAR = auto()


#SEPARADORES, como ; , ( ) { } [ ]

    #define token para abre parenteses direita )
    PARENTESES_DIREITO = auto()
    #define token para abre parenteses esquerda (
    PARENTESES_ESQUERDO = auto()
    #chaves para definir blocos de código, como em arrays ou listas.
    CHAVES_ESQUERDO = auto()
    #chaves para definir blocos de código, como em arrays ou listas.
    CHAVES_DIREITO = auto()
    #colchetes para definir blocos de código, como em arrays ou listas.
    COLCHETES_ESQUERDO = auto()
    #colchetes para definir blocos de código, como em arrays ou listas.
    COLCHETES_DIREITO = auto()
    #virgula para separar elementos em listas, arrays ou parâmetros de funções.
    VIRGULA = auto()


    


#tokens de operadores, como +, -, *, /, =, ==, !=

    MAIS = auto()

    MENOS = auto()

    MULTIPLICACAO = auto()

    BARRA = auto()

    ESTRELA = auto()

    MAIOR = auto()

    MAIOR_IGUAL = auto()

    MENOR = auto()

    MENOR_IGUAL = auto()

    IGUAL_OUTRO = auto()

    IGUAL_IGUAL = auto()

    DIFERENTE = auto()

    



@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object = None
    line: int = 1

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"


# classe token, que representa cada token encontrado no código fonte, com seu tipo, lexema, valor literal e número da linha onde foi encontrado.


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        # definese source e inicializa as variáveis necessárias para o processo de análise léxica, como a lista de tokens, os índices de início e fim do token atual e o número da linha.

    def scanear_tokens(self):
        while not self.se_fim():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    # funcao que percorre o código fonte, chamando o método scan_token para cada token encontrado, até chegar ao final do arquivo. No final, adiciona um token EOF para indicar o fim do arquivo.

    def se_fim(self):
        return self.current >= len(self.source)

    # : funcao que verifica se o índice atual ultrapassou o comprimento do código fonte, indicando que chegamos ao final do arquivo.

    def avancar(self):
        char = self.source[self.current]
        self.current += 1
        return char
    
    # aqui onde o método avancar é responsável por avançar o índice atual e retornar o caractere correspondente, permitindo que o lexer percorra o código fonte.

    def add_token(self, type_, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

        # adiciona um token à lista de tokens, criando uma instância da classe Token com o tipo, lexema, valor literal e número da linha correspondentes.

    def scan_token(self):
        char = self.avancar()

        if char.isalpha() or char == "_":
            self.identifier()
        elif char.isdigit():
            self.number()
        elif char == "+":
            self.add_token(TokenType.MAIS)
        elif char == "-":
            self.add_token(TokenType.MENOS)
        elif char == "*":
            self.add_token(TokenType.MULTIPLICACAO)
        elif char == "/":
            self.add_token(TokenType.BARRA)
        elif char == "!=":
            self.add_token(TokenType.DIFERENTE)
        elif char == "==":
            self.add_token(TokenType.IGUAL_IGUAL)
        elif char == "=":
            self.add_token(TokenType.IGUAL_OUTRO)
        elif char == ">":
            self.add_token(TokenType.MAIOR)
        elif char == ">=":
            self.add_token(TokenType.MAIOR_IGUAL)
        elif char == "<":
            self.add_token(TokenType.MENOR)
        elif char == "<=":
            self.add_token(TokenType.MENOR_IGUAL)
        elif char == '"':
            self.string()
        elif char == ",":
            self.add_token(TokenType.VIRGULA)
        elif char in ["(", ")"]:
            self.add_token(TokenType.PARENTESES_ESQUERDO if char == "(" else TokenType.PARENTESES_DIREITO)
        elif char in ["{", "}"]:
            self.add_token(TokenType.CHAVES_ESQUERDO if char == "{" else TokenType.CHAVES_DIREITO)
        elif char in ["[", "]"]:
            self.add_token(TokenType.COLCHETES_ESQUERDO if char == "[" else TokenType.COLCHETES_DIREITO)
        elif char in ["{", "}", "[", "]", ";", ","]:
            self.add_token(TokenType.SEPARADORES)
        elif char in [" ", "\r", "\t"]:
            pass
        elif char == "\n":
            self.line += 1
        else:
            raise Exception(f"Caractere inesperado na linha {self.line}: {char}")

        # valida se o caractere atual é uma letra ou um sublinhado, indicando o início de um identificador ou palavra reservada, ou se é um dígito, indicando o início de um número. Também verifica se o caractere é um operador ou separador, ou se é um espaço em branco ou nova linha, e trata cada caso adequadamente. Se encontrar um caractere inesperado, lança uma exceção.

    def number(self):
        while not self.se_fim() and self.source[self.current].isdigit():
            self.avancar()

        text = self.source[self.start : self.current]
        self.add_token(TokenType.NUMERO, int(text))

        # define o método number, que percorre os dígitos do número, avançando o índice atual até encontrar um caractere que não seja um dígito. Em seguida, extrai o texto correspondente ao número e adiciona um token do tipo NUMBER à lista de tokens, com o valor literal convertido para inteiro.

    def identifier(self):
        while not self.se_fim() and (
            self.source[self.current].isalnum() or self.source[self.current] == "_"
        ):
            self.avancar()

        text = self.source[self.start : self.current]

        if text == "var":
            self.add_token(TokenType.VARIAVEL)
        elif text == "se":
            self.add_token(TokenType.SE)
        elif text == "senao":
            self.add_token(TokenType.SENAO)
        elif text == "faca":
            self.add_token(TokenType.FACA)
        elif text == "enquanto":
            self.add_token(TokenType.ENQUANTO)
        elif text == "funcao":
            self.add_token(TokenType.FUNCAO)
        elif text == "retorno":
            self.add_token(TokenType.RETORNO)
        elif text == "ain_talon":
            self.add_token(TokenType.QUEBRAR)
        elif text == "trocar":
            self.add_token(TokenType.TROCAR)
        else:
            self.add_token(TokenType.IDENTIFICADOR)

            # define o indentificador, que percorre os caracteres alfanuméricos e sublinhados, avançando o índice atual até encontrar um caractere que não seja válido para um identificador. Em seguida, extrai o texto correspondente ao identificador e verifica se é uma palavra reservada (como "var" ou "if"), adicionando o token correspondente à lista de tokens. Se não for uma palavra reservada, adiciona um token do tipo IDENTIFIER.

            # classe lexer, que é responsável por analisar o código fonte e gerar os tokens correspondentes, utilizando métodos para identificar números, identificadores, operadores e separadores.
