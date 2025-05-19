import unittest
import io
from common import Token, TokenTypes
from Lexer import Lexer
import Interpreter

class LexerTests(unittest.TestCase):
    def testEmpty(self) -> None:
        output: list[Token] = Lexer(io.StringIO(" \t\n")).lex()
        self.assertEqual(first=output, second=[])

    def testSingleDigit(self) -> None:
        output: list[Token] = Lexer(io.StringIO("3")).lex()
        self.assertEqual(first=output, second=[Token(TokenTypes.INT, 3)])

    def testMultiDigit(self) -> None:
        output: list[Token] = Lexer(io.StringIO("12")).lex()
        self.assertEqual(first=output, second=[Token(TokenTypes.INT, 12)])
    
    def testOps(self) -> None:
        operators: str = "+-*/"
        output: list[Token] = Lexer(io.StringIO(operators)).lex()
        self.assertEqual(first=output, second=[Token(TokenTypes.OP, c) for c in operators])

    def testMixed(self) -> None:
        output: list[Token] = Lexer(io.StringIO("3 +5")).lex()
        
        expected: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 5),
            ]
        self.assertEqual(first=output, second=expected)

    def testUnknown(self) -> None:
        with self.assertRaises(AssertionError):
            Lexer(io.StringIO(".")).lex()

class InterpreterTests(unittest.TestCase):
    def testAdd(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 5),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 8
        self.assertEqual(first=output, second=expected)
    
    def testSub(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.OP, "-"),
            Token(TokenTypes.INT, 5),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = -2
        self.assertEqual(first=output, second=expected)

    def testMulti(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 9), 
            Token(TokenTypes.OP, "-"),
            Token(TokenTypes.INT, 5),
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 3),
            Token(TokenTypes.OP, "+"),
            Token(TokenTypes.INT, 11),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 9 - 5 + 3 + 11
        self.assertEqual(first=output, second=expected)
        
if __name__ == "__main__":
    unittest.main()