import unittest
import io
from common import Token, TokenTypes
import Lexer
import Interpreter

class LexerTests(unittest.TestCase):
    def testEmpty(self) -> None:
        output: list[Token] = Lexer.lex(io.StringIO(" \t\n"))
        self.assertEqual(first=output, second=[])

    def testSingleDigit(self) -> None:
        output: list[Token] = Lexer.lex(io.StringIO("3"))
        self.assertEqual(first=output, second=[Token(Lexer.TokenTypes.INT, 3)])

    def testMultiDigit(self) -> None:
        output: list[Token] = Lexer.lex(io.StringIO("12"))
        self.assertEqual(first=output, second=[Token(Lexer.TokenTypes.INT, 12)])
    
    def testOp(self) -> None:
        output: list[Token] = Lexer.lex(io.StringIO("+"))
        self.assertEqual(first=output, second=[Token(Lexer.TokenTypes.OP, "+")])

    def testMixed(self) -> None:
        output: list[Token] = Lexer.lex(io.StringIO("3 +5"))
        
        expected: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 5),
            ]
        self.assertEqual(first=output, second=expected)

    def testUnknown(self) -> None:
        with self.assertRaises(AssertionError):
            Lexer.lex(io.StringIO("."))

class InterpreterTests(unittest.TestCase):
    def testAdd(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 5),
            ]
        output: int = Interpreter.interpret(tokens)
        excepted: int = 8
        self.assertEqual(first=output, second=excepted)
    
    def testSub(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "-"),
            Token(TokenTypes.INT, 5),
            ]
        output: int = Interpreter.interpret(tokens)
        excepted: int = -2
        self.assertEqual(first=output, second=excepted)

if __name__ == "__main__":
    unittest.main()