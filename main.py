import Lexer
import Interpreter
import io
from common import Token

while True:
    tokens: list[Token] = Lexer.lex(io.StringIO(input("calc> ")))
    print(tokens)
    print(Interpreter.interpret(tokens))