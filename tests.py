import unittest
import io
from common import Token, TokenTypes, OPERATORS, PARENS
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
        output: list[Token] = Lexer(io.StringIO("".join(OPERATORS.keys()))).lex()
        self.assertEqual(first=output, second=[i for i in OPERATORS.values()])

    def testParen(self) -> None:
        output: list[Token] = Lexer(io.StringIO("".join(PARENS.keys()))).lex()
        self.assertEqual(first=output, second=[i for i in PARENS.values()])

    def testMixed(self) -> None:
        output: list[Token] = Lexer(io.StringIO("(3 +55)")).lex()
        
        expected: list[Token] = [
            Token(TokenTypes.LPAREN, "("),
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 55),
            Token(TokenTypes.RPAREN, ")"),
            ]
        self.assertEqual(first=output, second=expected)

    def testUnknown(self) -> None:
        with self.assertRaises(AssertionError):
            Lexer(io.StringIO(".")).lex()

class InterpreterTests(unittest.TestCase):
    def testAdd(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 5),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 8
        self.assertEqual(first=output, second=expected)
    
    def testSub(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.MINUS, "-"),
            Token(TokenTypes.INT, 5),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = -2
        self.assertEqual(first=output, second=expected)
    
    def testMulti(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.MUL, "*"),
            Token(TokenTypes.INT, 5),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 15
        self.assertEqual(first=output, second=expected)

    def testDiv(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 6), 
            Token(TokenTypes.DIV, "/"),
            Token(TokenTypes.INT, 2),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: float = 3.0
        self.assertEqual(first=output, second=expected)

    def testAssoc(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 9), 
            Token(TokenTypes.MINUS, "-"),
            Token(TokenTypes.INT, 5),
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 3),
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 11),
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 9 - 5 + 3 + 11
        self.assertEqual(first=output, second=expected)
    
    def testPrecedence(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 7), 
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 5),
            Token(TokenTypes.MUL, "*"),
            Token(TokenTypes.INT, 2)
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: int = 7 + 5 * 2
        self.assertEqual(first=output, second=expected)

    def testParen(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 7), 
            OPERATORS["+"],
            Token(TokenTypes.INT, 3),
            OPERATORS["*"],
            PARENS["("],
            Token(TokenTypes.INT, 10),
            OPERATORS["/"],
            PARENS["("],
            Token(TokenTypes.INT, 12),
            OPERATORS["/"],
            PARENS["("],
            Token(TokenTypes.INT, 3),
            OPERATORS["+"],
            Token(TokenTypes.INT, 1),
            PARENS[")"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 1),
            PARENS[")"],
            PARENS[")"]
            ]
        output: int|float = Interpreter.interpret(tokens)
        expected: float = 7 + 3 * (10 / (12 / (3 + 1) - 1))
        self.assertEqual(first=output, second=expected)

if __name__ == "__main__":
    unittest.main()