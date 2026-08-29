from enum import Enum, auto


class TokenType(Enum):
    # Palavra reservada para declaração de variáveis.
    # Exemplo: var x = 10;
    VAR = auto()

    # Palavra reservada para estruturas condicionais.
    # Exemplo: if (x > 10)
    IF = auto()

    # Nome dado pelo programador para variáveis,
    # funções, classes, etc.
    # Exemplos: x, contador, soma, minhaFuncao
    IDENTIFIER = auto()

    # Valores numéricos.
    # Exemplos: 10, 3.14, 42
    NUMBER = auto()

    # Cadeias de caracteres delimitadas por aspas.
    # Exemplos: "Olá Mundo", "Pedro"
    STRING = auto()

    # Operadores da linguagem.
    # Exemplos: +, -, *, /, =, ==, !=, <, >
    OPERATOR = auto()

    # Símbolos que organizam a sintaxe.
    # Exemplos: ; , ( ) { } [ ]
    SEPARATOR = auto()

    # Marca o final do arquivo ou entrada.
    # Facilita o parser saber quando encerrar a análise.
    EOF = auto()

    # aqui onde sera definido os tokens, como palavras reservadas, operadores, etc.

class Token:
    def __init__(self, type_, lexeme, literal=None, line=1):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

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
        while not self.is_at_end():
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
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

        # adiciona um token à lista de tokens, criando uma instância da classe Token com o tipo, lexema, valor literal e número da linha correspondentes.

    def scan_token(self):
        char = self.avancar()

        if char.isalpha() or char == "_":
            self.identifier()
        elif char.isdigit():
            self.number()
        elif char in ["+", "-", "*", "/", "=", "!", "<", ">"]:
            self.add_token(TokenType.OPERATOR)
        elif char in ["(", ")", "{", "}", "[", "]", ";", ","]:
            self.add_token(TokenType.SEPARATOR)
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

        text = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, int(text))

        # define o método number, que percorre os dígitos do número, avançando o índice atual até encontrar um caractere que não seja um dígito. Em seguida, extrai o texto correspondente ao número e adiciona um token do tipo NUMBER à lista de tokens, com o valor literal convertido para inteiro.

    def identifier(self):
        while not self.se_fim() and (
            self.source[self.current].isalnum() or self.source[self.current] == "_"
        ):
            self.avancar()

        text = self.source[self.start:self.current]

        if text == "var":
            self.add_token(TokenType.VAR)
        elif text == "if":
            self.add_token(TokenType.IF)
        else:
            self.add_token(TokenType.IDENTIFIER)

            # define o indentificador, que percorre os caracteres alfanuméricos e sublinhados, avançando o índice atual até encontrar um caractere que não seja válido para um identificador. Em seguida, extrai o texto correspondente ao identificador e verifica se é uma palavra reservada (como "var" ou "if"), adicionando o token correspondente à lista de tokens. Se não for uma palavra reservada, adiciona um token do tipo IDENTIFIER.

            # classe lexer, que é responsável por analisar o código fonte e gerar os tokens correspondentes, utilizando métodos para identificar números, identificadores, operadores e separadores.