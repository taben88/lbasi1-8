from Lexer import Lexer
import Interpreter
import io
from common import Token

while True:
    lexer = Lexer(io.StringIO(input("calc> ")))
    tokens: list[Token] = lexer.lex()
    print(tokens)
    print(Interpreter.interpret(tokens))