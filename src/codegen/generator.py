from src.parser.ast import (
    Bloco,
    Faca_enquanto,
    Se,
    Var,
    Variable,
    funcao,
    Enquanto,
    Declaracao,
    Binary,
    Unary,
    Literal,
    Grouping,
    Atribuicao,
    Declaracao,
    ExpressaoStatement,
    Print,
    retorno,
    Trocar,
    quack,
    principal,
    Vetor,
    Quebrar,
    AcessarVetor,
    chamar,
)

##gerador de codigo, vai chamar todas as classes da AST com regras de parser, e retornar os valores na tela, vai instanciar junto dando o no e retornando valores no gerador de codigo transmitindo os passos paraa  maquina virtual
##Teste das expressoes em teste_gerador.py


class codegen:
    ###INFRAESTRUTURA DO CODEGEN!!
    ##Inicio do codegen, chamando os metodos da ast e criando a infraestrutura do gerador de codigo
    def __init__(self):
        self.codigo = []
        self.contador = 0
        self.fim_do_laco = []

    def novo_contador(self):
        label = f"L{self.contador}"
        self.contador += 1
        return label

    def identificar_contador(self, label):
        self.codigo.append(f"{label}:\n")

    ##emissao de argumentos em funcao da instrucso
    def emit(self, instrucao, argumentos=None):
        if argumentos is not None:
            self.codigo.append(f"{instrucao} {argumentos}\n")
        else:
            self.codigo.append(f"{instrucao}\n")

    ##respostas de retorno do codigo gerado
    # vai chamar e isntanciar cada no da AST com a funcao de geracao do codigo, sempre com os valores dos nos da AST
    def gerar_resposta(self, no):

        if isinstance(no, Binary):
            return self.gerar_binary(no)

        if isinstance(no, Unary):
            return self.gerar_unario(no)

        if isinstance(no, Literal):

            return self.gerar_literal(no)

        if isinstance(no, Grouping):
            return self.gerar_grouping(no)

        if isinstance(no, Variable):
            return self.gerar_variable(no)

        if isinstance(no, Atribuicao):
            return self.gerar_atribuicao(no)

        if isinstance(no, ExpressaoStatement):
            return self.gerar_expressaostatement(no)

        if isinstance(no, chamar):
            return self.gerar_chamar(no)

        if isinstance(no, Print):
            return self.gerar_print(no)

        if isinstance(no, principal):
            return self.gerar_principal(no)

        if isinstance(no, Var):
            return self.gerar_var(no)

        if isinstance(no, Bloco):
            return self.gerar_bloco(no)

        if isinstance(no, Se):
            return self.gerar_se(no)

        if isinstance(no, Enquanto):
            return self.gerar_enquanto(no)

        if isinstance(no, Faca_enquanto):
            return self.gerar_faca_enquanto(no)

        if isinstance(no, funcao):
            return self.gerar_funcao(no)

        if isinstance(no, retorno):
            return self.gerar_retorno(no)

        if isinstance(no, Trocar):
            return self.gerar_trocar(no)

        ## if isinstance(no, Trocar):
        #   for elemento in no:
        #      self.gerar_resposta(elemento)
        # return

        if isinstance(no, quack):
            return self.gerar_quack(no)

        if isinstance(no, Vetor):
            return self.gerar_vetor(no)

        if isinstance(no, Quebrar):
            return self.gerar_quebrar(no)

        if isinstance(no, AcessarVetor):
            return self.gerar_acessar_vetor(no)

        if isinstance(no, Declaracao):
            return self.gerar_declaracao(no)

        raise TypeError(f"No nao suportado: {type(no).__name__}")

    # +, -, *, /, =, ==, !=, >, >=. <=, !=

    ##Geração das funcoes de reposta, no caso com expressoes binarias as operações
    #

    def gerar_binary(self, no):

        self.gerar_resposta(no.left)
        self.gerar_resposta(no.right)

        operacoes = {
            "+": "ADICAO",
            "-": "SUBTRACAO",
            "*": "MULTIPLICACAO",
            "/": "DIVISAO",
            "!=": "DIFERENTE",
            "<=": "MENOR_IGUAL",
            ">=": "MAIOR_IGUAL",
            "=": "IGUAL_OUTRO",
            "==": "IGUAL_IGUAL",
            ">": "MAIOR",
            "<": "MENOR",
        }

        ##pega as operações e verifica se ha operações com base na leitura do codigo antes de retornar
        ## ao gerador, se nao tiver operador, reotrna raise
        instrucao = operacoes.get(no.operator.lexeme)
        if instrucao is None:
            raise ValueError(f"operador desconhecido {no.operator}")

        self.emit(instrucao)

        return no

    ##outras funcoes de geracao de codigo
    def gerar_unario(self, no):
        self.gerar_resposta(no.right)

        operacoes = {"-": "NEGATE", "!": "NOT"}

        ##pega as operações e verifica se ha operações com base na leitura do codigo antes de retornar
        ## ao gerador, se nao tiver operador, reotrna raise
        instrucao = operacoes.get(no.operator.lexeme)
        if instrucao is None:
            raise ValueError(f"operador desconhecido {no.operator}")

        self.emit(instrucao)

    def gerar_literal(self, no):
        if isinstance(no.value, str):
            self.emit("STRING", no.value)
        else:
            self.emit("NUMBER", no.value)

    def gerar_grouping(self, no):
        self.gerar_resposta(no.expression)

    def gerar_variable(self, no):
        self.emit("LOAD", no.name.lexeme)

    def gerar_atribuicao(self, no):
        self.gerar_resposta(no.value)
        self.emit("STORE", no.name.lexeme)

    def gerar_declaracao(self, no):
        self.emit("DECLARE")

    def gerar_expressaostatement(self, no):
        self.gerar_resposta(no.expression)
        self.emit("POP")

    def gerar_print(self, no):
        self.gerar_resposta(no.expression)
        self.emit("PRINT")

    def gerar_quack(self, no):
        self.gerar_resposta(no.expression)
        self.emit("QUACK")

    def gerar_var(self, no):
        if no.initializer is None:
            self.emit("NONE")
        else:
            self.gerar_resposta(no.initializer)

        self.emit("DECLARE", no.name.lexeme)

    def gerar_bloco(self, no):
        self.emit("BLOC_BEGIN")
        for declaracao in no.statements:
            self.gerar_resposta(declaracao)
        self.emit("END_BLOC")

    def gerar_se(self, no):
        senao = self.novo_contador()
        fim = self.novo_contador()

        self.gerar_resposta(no.condition)
        self.emit("JUMP_IF_FALSE", senao)

        self.gerar_resposta(no.entao)
        self.emit("JUMP", fim)

        self.identificar_contador(senao)

        if no.senao is not None:
            self.gerar_resposta(no.senao)

        self.identificar_contador(fim)

    def gerar_enquanto(self, no):
        ini = self.novo_contador()
        fim = self.novo_contador()
        self.fim_do_laco.append(fim)

        self.identificar_contador(ini)
        self.gerar_resposta(no.condition)
        self.emit("JUMP_IF_FALSE", fim)
        self.gerar_resposta(no.body)
        self.emit("JUMP", ini)
        self.identificar_contador(fim)

        self.fim_do_laco.pop()

    def gerar_faca_enquanto(self, no):
        ini = self.novo_contador()
        fim = self.novo_contador()
        self.fim_do_laco.append(fim)

        self.identificar_contador(ini)
        self.gerar_resposta(no.body)
        self.gerar_resposta(no.condition)
        self.emit("JUMP_IF_TRUE", ini)
        self.identificar_contador(fim)

        self.fim_do_laco.pop()

    def gerar_funcao(self, no):
        self.emit("FUNCTION", no.name.lexeme)
        for parametro in no.parametros:
            self.emit("PARAM", parametro.lexeme)
        self.gerar_resposta(no.body)

        self.emit("END_FUNCTION")

    def gerar_retorno(self, no):
        if no.value is not None:
            self.gerar_resposta(no.value)
        self.emit("RETURN")

    def gerar_chamar(self, no):
        self.emit("CALL")
        self.gerar_resposta(no.callee)
        for argumentos in no.argumentos:
            self.gerar_resposta(argumentos)
        self.emit("END_CALL")

    def gerar_trocar(self, no):
        fim = self.novo_contador()
        self.fim_do_laco.append(fim)

        for caso in no.casos:
            proximo = self.novo_contador()

            if caso.value is not None:
                self.gerar_resposta(no.condition)
                self.gerar_resposta(caso.value)
                self.emit("IGUAL_IGUAL")
                self.emit("JUMP_IF_FALSE", proximo)

            for stmt in caso.body:
                self.gerar_resposta(stmt)

            self.emit("JUMP", fim)
            self.identificar_contador(proximo)

        self.identificar_contador(fim)
        self.fim_do_laco.pop()

    def gerar_quebrar(self, no):
        if not self.fim_do_laco:
            raise SyntaxError("'quebrar' fora de laço ou trocar")
        self.emit("JUMP", self.fim_do_laco[-1])

    def gerar_vetor(self, no):
        for elementos in no.elements:
            self.gerar_resposta(elementos)
        self.emit("VEC_GERATOR")

    def gerar_acessar_vetor(self, no):
        self.gerar_resposta(no.value)
        self.gerar_resposta(no.index)
        self.emit("VEC_VALOR")

    def gerar_principal(self, no):
        self.emit("PRINCIPAL")
        corpo = no.body
        self.gerar_resposta(corpo)

        return
