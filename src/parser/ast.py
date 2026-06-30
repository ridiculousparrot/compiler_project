from dataclasses import dataclass
from abc import ABC


class Expr(ABC):
    pass


# Classe base e abstrata para todas as expressões na árvore de sintaxe abstrata (AST). Ela serve como um tipo genérico para representar qualquer expressão, permitindo que outras classes específicas de expressões herdem dela e sejam tratadas de forma polimórfica. Assim, trabalhando com uma hierarquia de classes que representam diferentes tipos de expressões, como operações binárias, unárias, literais, agrupamentos, etc., todas derivando da classe base Expr.


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: "Token"
    right: Expr
    # operador binário, como +, -, *, /, etc., que tem um operando à esquerda e outro à direita. Assim, trabalhando com dois operandos e um operador para realizar uma operação matemática ou lógica entre eles.


@dataclass(frozen=True)
class Unary(Expr):
    operator: "Token"
    right: Expr


# operador unário, como - ou !, que tem um operando à direita e nenhum à esquerda. Assim, trabalhandso com um operador e um operando para realizar uma operação matemática ou lógica sobre ele, como negação ou inversão de valor.


@dataclass(frozen=True)
class Literal(Expr):
    value: object


# valor literal, como números, strings, booleanos, etc., que representa um valor fixo no código fonte. Assim, trabalhando com um valor específico que pode ser usado diretamente em expressões ou atribuições, sem a necessidade de avaliação adicional.


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr


# expressão agrupada, como (1 + 2), que tem uma expressão dentro de parênteses para indicar a precedência das operações. Assim, trabalhando com uma expressão que é avaliada como um todo, garantindo que as operações dentro dos parênteses sejam realizadas antes de outras operações fora deles.
