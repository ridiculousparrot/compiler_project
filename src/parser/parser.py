import types
from xmlrpc.client import Binary
from compiler_project.src.lexer.lexer import TokenType
from compiler_project.src.utils.errors import parserError

class Parser:   
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0    

    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current -1]
    
    def end(self):
        return self.peek().type == TokenType.EOF
    
    def advance(self):
        if not self.end():
            self.current += 1

        return self.previous()
    
    def verify_end(self, type_):
        if self.end():
            return False
        
        return self.peek().type == type_
    
    def parser_math(self):
       for type_ in types:
           if self.verify_end(type_):
               self.advance()
               return True
           return False
    
    def costume(self, type_, message):
        if self.verify_end(type_):
            return self.advance()
        
        raise parserError(self.peek().line, message)
    
    def parser_gram(self):

        statement = []

        while not self.end():
            statement.append(self.parser_math)

        return statement
    
    def expression(self):  
      return self.parser_math() 

    def varDeclaration(self):
        name = self.costume(tokenType.IDENTIFIER, "Esperado um identificador após a palavra reservada 'var'.")
        self.costume(tokenType.EQUAL, "Esperado '=' após o identificador.")

        inicializador = self.expression()   
        self.costume(tokenType.SEPARATOR, "Esperado ';' após a declaração da variável.")

        return self.varDeclaration(name, inicializador)
  
    def term(self):
        expr = self.factor()

        while self.verify_end(tokenType.PLUS, tokenType.MINUS): 
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr

