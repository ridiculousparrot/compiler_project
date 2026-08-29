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
    
@dataclass(frozen=True)
class definirAST:
    expression: Expr
    print: Expr

@dataclass(frozen=True)
class identificadorVariavel:
    expression: Expr
    print: Expr


