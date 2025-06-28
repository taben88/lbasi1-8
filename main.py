from Lexer import Lexer
from Parser import Parser
import io
from common import Token, Visitor

while True:
    lexer = Lexer(io.StringIO(input("calc> ")))
    tokens: list[Token] = lexer.lex()
    root = Parser(tokens).parse()
    print(Visitor().visit(root))