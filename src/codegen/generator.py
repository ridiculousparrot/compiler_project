from parser.ast import Bloco, Faca_enquanto, Se, Var, Variable, funcao, Enquanto, Declaracao, Binary, Unary, Literal, Grouping, Atribuicao, Declaracao, ExpressaoStatement, Print, retorno


##gerador de codigo, vai chamar todas as classes da AST com regras de parser, e retornar os valores na tela, vai instanciar junto dando o no e retornando valores no gerador de codigo 

class codegen:

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

        if isinstance(no, Declaracao):
            return self.gerar_declaracao(no)

        if isinstance(no, ExpressaoStatement):
            return self.gerar_expressaostatement(no)

        if isinstance(no, Print):
            return self.gerar_print(no)

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

        raise TypeError(f"No nao suportado: {type(no).__name__}")

#+, -, *, /, =, ==, !=, >, >=. <=, !=
    def gerar_binary(self, no):
        esquerda = self.gerar_resposta(no.left)
        direita = self.gerar_resposta(no.right)

        if no.operador == "+":
            self.emit("ADICAO")
        elif no.operador =="-":
            self.emit("SUBTRACAO")
        elif no.operador == '*':
            self.emit("MULTIPLICACAO")
        elif no.operador =="/":
            self.emit("DIVISAO")
        elif no.operador == "!=":
            self.emit("DIFERENTE")
        elif no.operador == "<=":
            self.emit("MENOR_IGUAL")
        elif no.operador == ">=":
            self.emit("MAIOR_IGUAL")
        elif no.operador == "=":
            self.emit("IGUAL_OUTRO")
        elif no.operador == "==":
            self.emit("IGUAL_IGUAL")
        elif no.operador == ">":
            self.emit("MAIOR")
        elif no.operador == "<":
            self.emit("MENOR")

        return None

    def gerar_unario(self, no):
        direta = self.gerar_resposta(no.right)

        return no