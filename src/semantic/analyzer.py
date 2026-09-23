from src.lexer.lexer import TokenType
from src.parser.ast import Literal, Grouping, Unary, Binary, Print, Var, Faca_enquanto, Se, Enquanto, Bloco, retorno, ExpressaoStatement, Variable, Atribuicao, funcao, chamar, Quebrar, Trocar, Vetor, principal

class retornarException(Exception):
    def __init__(self, value):
        self.value = value
class Interpretador:

    def __init__(self):
        #define o ambiente da linguagem e guarda espaco para declaracoes de variaveis
        self.ambiente = {}
        self.tem_principal = False

    #cria a classse interpretador, que é responsável por avaliar e executar as expressões da linguagem.
    def analisar_arvore_sintatica(self, statements):
        encontrada = False
        for declaracao in statements:
         if isinstance(declaracao, principal):
            if encontrada:
                raise Exception("O programa não pode possuir mais de uma principal.")
            encontrada = True

        if not encontrada:
         raise Exception("Erro semântico: o programa deve possuir uma main.")
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
        if isinstance(expr, Vetor):
            return self.visitar_vetor(expr)
        if isinstance(expr, Atribuicao):
            return self.visitar_atribuicao(expr)
        if isinstance(expr, chamar):
            return self.visitar_chamar(expr)

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

            case TokenType.DIFERENTE:
                 return esquerda != direita

            case TokenType.IGUAL_IGUAL:
                return esquerda == direita

        return None

    #aqui comeca a forma como a linguagem vai interpretar as expressoes binarias, aplicando o operador binário apropriado aos valores dos operandos esquerdo e direito e retornando o resultado da operação.

#funcao responsavel por executar os statements, chamando o metodo accept para que o statement aceite o interpretador e execute a ação correspondente.
    def executar(self, stmt):
        if isinstance(stmt, Print):
            return self.visitarPrintStmt(stmt)
        if isinstance(stmt, Var):
            return self.visitar_declaracao_variavel(stmt)
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
        if isinstance(stmt, funcao):
            return self.visitar_funcao(stmt)
        if isinstance(stmt, Trocar):
            return self.visitar_trocar(stmt)
        if isinstance(stmt, principal):
            return self.visitar_principal(stmt)
        if isinstance(stmt, Quebrar):
            return None
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
    def interpretar_funcao(self, funcao_stmt, argumentos):
        ambiente_anterior = self.ambiente
        self.ambiente = dict(ambiente_anterior)

        for param, valor in zip(funcao_stmt.parametros, argumentos):
            self.ambiente[param.lexeme] = valor

            resultado = None
            try: 
                for statement in funcao_stmt.body.statements:
                    resultado = self.executar(statement)
            finally:self.ambiente = ambiente_anterior

            return resultado 
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

        if isinstance(value, list):
            return ',' .join(self.stringify(v) for v in value)

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
         while True:
                   for declaracao in stmt.body:
                       self.executar(declaracao)
                   if not self.seVerdadeiro(self.avaliar(stmt.condition)):
                    break

#visitar a condicao faca enquanto, quando executa o circulo do while, verrifica a condicao, se for verdadeira repetete o processo, caso falsa, encerra o loop
    def visitar_faca_enquanto(self, stmt):
          while True:
            for declaracao in stmt.body:
                self.executar(declaracao)

            if not self.seVerdadeiro(self.avaliar(stmt.condition)):
                break

    def visitar_funcao(self, stmt):
        #aqui a funcao vai retornar o valor da funcao, que pode ser None caso a expressao digitada nao tenha valor
       self.ambiente[stmt.name.lexeme] = stmt
       return None

#regra de retur, define valor de retorno = nulo, se o valor do statemnt nao for nulo, ele avalia noamente o valor da statement, e retorna 
# o valor da expressao digitada, caso nao tenha valor, retorna nulo
    def visitar_retorno(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.avaliar(stmt.value)
        raise retornarException(value)

##Visitar variavel nessecario para ler o que e variabel, a atribuicao do seu nome com if, chamando a expressao expr, variavel nao perternce ao grupo de statements
#se nao estiver no ambiente retorna exception para que nao seja declarada
#retorna o ambimente com o nome dela caso nao cair na chamada condicional



    def visitar_bloco(self, stmt):
#Executa sequencialmente todas as instruções pertencentes a um bloco.

    #O método percorre a lista de instruções armazenada em `stmt.statements`
    #e envia cada instrução para o método `executar()`. O resultado da última
    #instrução executada é armazenado e retornado ao final.

    #Parâmetros:
        #stmt:
       #     Nó da AST que representa um bloco de instruções. Esse nó deve
      #      possuir o atributo `statements`, contendo as instruções que
     #       fazem parte do bloco.

    #Retorno:
      #  O resultado da última instrução executada no bloco. Caso o bloco
     #   não possua instruções, retorna `None`.

    #Funcionamento:
      #  1. Inicializa `resultado` com `None`.
     #   2. Percorre todas as instruções do bloco.
    #    3. Executa cada instrução utilizando `self.executar()`.
   #     4. Atualiza `resultado` com o retorno da instrução atual.
  #      5. Retorna o resultado da última instrução.

 #   Exemplo:
#        Um bloco como:

            #{
            #    x = 10;
           #     y = 20;
          #      imprimir(y);
         #   }

        #terá suas instruções executadas na ordem em que aparecem.
    
        resultado = None
        for statement in stmt.statements:
            resultado = self.executar(statement)
        return resultado 



    def visitar_chamar(self, expr):
     #     Avalia e executa uma chamada de função representada na AST.

    #O método primeiro avalia a expressão que representa a função a ser
    #chamada. Em seguida, verifica se o resultado é uma instância de
    #`funcao`. Caso seja, os argumentos fornecidos são avaliados e
    #associados aos respectivos parâmetros da função.

    #Durante a execução da função, um novo ambiente é criado a partir do
    #ambiente atual. Esse novo ambiente recebe os valores dos parâmetros,
    #permitindo que as variáveis utilizadas pela função sejam isoladas
    #do ambiente anterior.

    #Parâmetros:
       # expr:
         #   Nó da AST que representa uma chamada de função. Deve possuir:
        #        - `calle`: expressão que representa a função chamada;
       #         - `argumentos`: lista de expressões correspondentes aos
      #            argumentos fornecidos;
     #           - `paren.line`: linha em que o parêntese da chamada aparece.

    #Retorno:
        #O valor retornado pela função.

        #Caso a função não possua uma instrução `return`, o resultado será
        #`None`.

    #Exceções:
        #Exception:
            #Gerada quando o objeto avaliado em `expr.calle` não é uma
            #função ou quando a quantidade de argumentos fornecidos é
            #diferente da quantidade de parâmetros da função.

        #retornarException:
            # utilizada internamente para interromper a execução da função
            #quando uma instrução `return` é encontrada. O valor armazenado
           # nessa exceção é utilizado como resultado da chamada.

    #Funcionamento:
        #1. Avalia a expressão que representa a função.
        #2. Verifica se o resultado é uma função.
        #3. Avalia todos os argumentos da chamada.
        #4. Verifica se a quantidade de argumentos corresponde à quantidade
        #   de parâmetros.
        #5. Salva o ambiente atual.
        #6. Cria um novo ambiente para a execução da função.
        #7. Associa cada parâmetro ao argumento correspondente.
        #8. Executa o corpo da função.
       # 9. Captura `retornarException` para obter o valor de retorno.
      #  10. Restaura o ambiente anterior.
     #   11. Retorna o resultado da função.

    #Exemplo:
        #Para uma função:

           # funcao soma(a, b) {
          #      return a + b;
         #   }

        #e uma chamada:

        #    soma(10, 20);

       # os valores `10` e `20` são associados aos parâmetros `a` e `b`,
     #   respectivamente. A execução do corpo produz o valor `30`, que é
       # retornado pela chamada.
    
        chamar = self.avaliar(expr.callee)

        if not isinstance(chamar, funcao):
            raise Exception(f"so e possivel chamar funcoes na linha{expr.line}")

        argumentos = [self.avaliar(arg) for arg in expr.argumentos]

        if len(argumentos)!= len(chamar.parametros):
            raise Exception(
                F"Esperado {len(chamar.parametros)} argumentos mas recebeu"
                f"{len(argumentos)}, na linha {expr.paren.line}"

            )

        ambiente_anterior = self.ambiente 
        self.ambiente = dict(ambiente_anterior)

        for param, valor in zip(chamar.parametros, argumentos):
            self.ambiente[param.lexeme] = valor

        resultado = None

        try:
            self.executar(chamar.body)
        except retornarException as ret:
            resultado = ret.value
        finally:
            self.ambiente = ambiente_anterior

        return resultado

    def visitar_trocar(self,stmt):
        valor = self.avaliar(stmt.condition)

        for valor_caso, statements, in stmt.casos:
            if valor == valor_caso:
                for statement in statements:
                    self.executar(statement)
                return None
        return None 

    def visitar_vetor(self,expr):
        return [self.avaliar(elements) for elements in expr.elements]


    

    def visitar_principal (self, stmt):
        self.executar(stmt.body)
        


    def visitar_programa(self, expr):
     encontrou_principal = False

     for declaracao in expr.declaracoes:

        if isinstance(declaracao, principal):
            if encontrou_principal:
                raise Exception(
                    "O programa não pode possuir mais de uma principal."
                )

            encontrou_principal = True

     self.executar(declaracao)

     if not encontrou_principal:
        raise Exception(
            "O programa deve possuir uma principal."
        )

        
