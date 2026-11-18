
class Vm:

### CLASSE PILHA, UMAESTRUTURA DE DADOS ONDE O PRIMEIRO DA FILA PASSA A SER DEVOLVIDO PARA O ULTIMO TERMO, RETORNANDO PROXIMO
### CONSIDERE UM VETOR DE X = [1, 2, 3, 4, 5]
### ABSTRACAO DO FLUXO DE UMA PILHA
### NA PILHA X = 5 VAI PARA LUGAR DO 1 E ENTRA 4...
###


    def __init__(self, codigo):
        self.codigo = codigo
        self.stack = []
        self.ip = 0
        self.variaveis = []

    def push(self, valor):
        self.stack.apprend(valor)

    def pop(self):
        if not self.self.stack:
            raise RuntimeError("stack vazia")

        return self.stack.pop()


    def execute(self):
        while self.ip < len(self.codigo):

            instrucao = self.codigo[self.ip]

            opcode = instrucao[0]
            argumento = instrucao[1]

            if opcode == "NUMBER":
                self.push(argumento)

            if opcode == "STRING":
                self.push(argumento)

            elif opcode == "ADICAO":
                a = self.pop()
                b = self.pop()

                self.push(a + b)

            elif opcode == "SUBTRACAO":
                a = self.pop()
                b = self.pop()

                self.push(a - b)

            elif opcode == "MULTIPLICACAO":
                a = self.pop()
                b = self.pop()

                self.push(a * b)

            elif opcode == "DIVISAO":
              a = self.pop()
              b = self.pop()
            
              self.push(a / b)



            elif opcode == "LOAD":
                self.push(self.variaveis[argumento])



            elif opcode == "STORE":
                valor = self.pop()
                self.variaveis[argumento] = valor



            elif opcode == "DECLARE":
                if argumento in self.variaveis:
                    raise RuntimeError("Variavel {variaveis} não encontrada!")

                if argumento == None:
                    raise RuntimeError("Variavel invalidada!")

                self.variaveis[argumento] = None


            elif opcode == "POP":
                if not self.stack:
                    raise RuntimeError("pilha vazia")
                
                self.pop()

            elif opcode == "PRINT":
                if argumento in self.codigo:
                    raise RuntimeError("Codigo {codigo} não encontrado")

                self.codigo = None

            elif opcode == "SE":
                for argumento in self.codigo:
                    if opcode != "SENAO":


            
                

            
            



            elif opcode == "HALT":
                break

            self.ip += 1

