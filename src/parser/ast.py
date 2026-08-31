from dataclasses import dataclass
from abc import ABC


# Classe base e abstrata para todas as expressões na árvore de sintaxe abstrata (AST).
# Serve como um tipo genérico para representar qualquer expressão e permite que os
# nós específicos da árvore sejam tratados de forma polimórfica.
class Expr(ABC):
    pass


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: "Token"
    right: Expr
    # operador binário, como +, -, *, /, etc., que tem um operando à esquerda e outro à direita.


@dataclass(frozen=True)
class Unary(Expr):
    # Expressão unária que possui um operador e um único operando.
    # Exemplo: -x ou !y
    operator: "Token"
    right: Expr


@dataclass(frozen=True)
class Literal(Expr):
    # Valor literal fixo, como número, string, booleano ou nil.
    value: object


@dataclass(frozen=True)
class Grouping(Expr):
    # Expressão agrupada entre parênteses para definir precedência.
    expression: Expr


# classe onde trataremos a statement, praticamente na arvore sintatica, as
# statements possuem o papel de representar uma acao a ser executada
class stmt:
    pass


@dataclass(frozen=True)
class Expressao:
    expression: Expr


# expressao produz valor


@dataclass(frozen=True)
class Print:
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


@dataclass(frozen=True)
class identificadorVariavel:
    expression: Expr
    print: Expr


# neste ponto, a declaracao e adicionada varivavel como filho percetencte a familha
class Declaracao:
    pass


@dataclass(frozen=True)
class Var(Declaracao):
    name: Token
    initializer: Expr | None


##(aviso) nao e apenas um no na AST, mas sim apenas uma regra gramatical.
# AST continua organizada em STMT
