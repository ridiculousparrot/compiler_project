from src.codegen.generator import codegen
from src.parser.ast import Binary, Literal

gen = codegen()
no = Binary(Literal(5), "+", Literal(3))

codigo = "" \
"NUMBER 5\n" \
"NUMBER 3\n" \
"ADD\n"\

gen.gerar_resposta(no)

codigo_teste = "".join(gen.codigo)

assert codigo_teste == codigo, f"erro: codigo gerado não corresponde ao esperado.\nesperado:\n{codigo}\nGerado:\n{codigo_teste}]"
