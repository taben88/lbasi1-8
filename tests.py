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