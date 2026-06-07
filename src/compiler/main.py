from src.lexer.lexer import Lexer

source = "var x = 10 + 2;"

lexer = Lexer(source)
tokens = lexer.scan_tokens()

for token in tokens:
    print(token)