from dataclasses import dataclass
from abc import ABC
import token
from compiler_project.src.lexer.lexer import Token, TokenType



#EXPRESSOES 


# Classe base e abstrata para todas as expressões na árvore de sintaxe abstrata (AST).
# Serve como um tipo genérico para representar qualquer expressão e permite que os
# nós específicos da árvore sejam tratados de forma polimórfica.
class Expr(ABC):
    pass


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr
    # operador binário, como +, -, *, /, etc., que tem um operando à esquerda e outro à direita.


@dataclass(frozen=True)
class Unary(Expr):
    # Expressão unária que possui um operador e um único operando.
    # Exemplo: -x ou !y
    operator: Token
    right: Expr


@dataclass(frozen=True)
class Literal(Expr):
    # Valor literal fixo, como número, string, booleano ou nil.
    value: object


@dataclass(frozen=True)
class Grouping(Expr):
    # Expressão agrupada entre parênteses para definir precedência.
    expression: Expr

#aqui e onde ao inves de realuzar a declaracao de variavel. passa a acessar ela atraves do nome
#por isso justifica o IDENTIFIER como o nome de uma variavel e nao ela em si, papel do VAR
@dataclass(frozen=True)
class Variable(Expr):
    name:Token

#atribuicao de variavel, ex:
#x = 10
@dataclass(frozen=True)
class Atribuicao(Expr):
    name: Token
    value: Expr


#STATEMENTS E DECLARAÇÔES


# classe onde trataremos a statement, praticamente na arvore sintatica, as
# statements possuem o papel de representar uma acao a ser executada
@dataclass(frozen=True)
class Declaracao(ABC):
    pass 

# Uma expressão usada como statement:
#
# x + 10;

@dataclass(frozen=True)
class ExpressaoStatement(Declaracao):
    expression: Expr

# aqui ele pega o valor da expressao e faz alguma coisa

# exemplo de leitura de uma expressao
# IfStatement
# ├── condition
# │   └── BinaryExpression (>)
# │       ├── x
# │       └── 10
# └── body
#    └── AssignmentStatement
#        ├── x
#        └── 20


# statements = estado
# neste ponto, a declaracao e adicionada varivavel como filho percetencte a familha
# expressao produz valor

#printa na tela print;

@dataclass(frozen=True)
class Print(Declaracao):
    expression: Expr
#arquiteura na arvore sintatica para sua declaracao no token lexer
#Se
#├── condition
#│   └── x > 10
#│
#├── entao
#│   └── print "maior"
#│
#└── senao
#    └── print "menor"


#declaracao de variavel 
#var x = 10;
@dataclass(frozen=True)
class Var(Declaracao):
    name: Token
    #incializador da valor inicial a uma variavel, caso nao seja declarado, o valor da variavel sera None
    initializer: Expr | None

##(aviso) nao e apenas um no na AST, mas sim apenas uma regra gramatical.
# AST continua organizada em STMT

@dataclass(frozen=True)
class Bloco(Declaracao):
    statements: list[Declaracao]
# Bloco:
#
# {
#     print x;
#     var y = 20;
# }

@dataclass(frozen=True)
class Se(Declaracao):
    condition: Expr
    entao: Declaracao
    senao : Declaracao | None

# bloco se e senao

@dataclass(frozen=True)
class Enquanto(Declaracao):
    condition: Expr
    body: Declaracao
#bloco de while (nesse caso apenas o uso do while isolado)

#bloco do do e while, agora com a condicao no final, diferente do while que tem a condicao no inicio)
@dataclass(frozen=True)
class Faca_enquanto(Declaracao):
    body: Declaracao
    condition: Expr

#uma funcao em programacao significa um bloco de código que realiza uma tarefa específica e pode ser reutilizado em diferentes partes do programa. 
#a classe funcao representa a declaracao de uma funcao, corpo, nome e lista de parametros, que podem ser passados de funcao para funcao
@dataclass(frozen=True)
class funcao(Declaracao):
      body: Declaracao
      name:token
      list_param: list[Token]

#retorno de uma funcao que pode ser none caso a expressao digitada nao tenha valor
@dataclass(frozen=True)
class retorno(Declaracao):
      value: Expr | None
    

#STATEMENTS DE VARIAVEIS GLOBAIS E LOCAIS


