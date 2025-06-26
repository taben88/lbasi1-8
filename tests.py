import unittest
import io
from common import Token, TokenTypes, OPERATORS, PARENS, AST, Visitor, Printer
from Lexer import Lexer
from Parser import Parser
# import Interpreter

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

    def testReal(self) -> None:
        outputs: list[list[Token]] = [
            Lexer(io.StringIO(".123")).lex(),
            Lexer(io.StringIO("0.123")).lex(),
            Lexer(io.StringIO("555.")).lex()
        ]
        expected: list[list[Token]] = [
            [Token(TokenTypes.REAL, .123)],
            [Token(TokenTypes.REAL, .123)],
            [Token(TokenTypes.INT, 555.)]
        ]
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertEqual(first=outputs[i], second=expected[i])
    
    def testOps(self) -> None:
        output: list[Token] = Lexer(io.StringIO("".join(OPERATORS.keys()))).lex()
        self.assertEqual(first=output, second=[i for i in OPERATORS.values()])

    def testParen(self) -> None:
        output: list[Token] = Lexer(io.StringIO("".join(PARENS.keys()))).lex()
        self.assertEqual(first=output, second=[i for i in PARENS.values()])

    def testMixed(self) -> None:
        output: list[Token] = Lexer(io.StringIO("(3 +55)")).lex()
        
        expected: list[Token] = [
            PARENS["("],
            Token(TokenTypes.INT, 3), 
            OPERATORS["+"],
            Token(TokenTypes.INT, 55),
            PARENS[")"],
            ]
        self.assertEqual(first=output, second=expected)

    def testUnknown(self) -> None:
        with self.assertRaises(AssertionError):
            Lexer(io.StringIO(".")).lex()

# class InterpreterTests(unittest.TestCase):
#     def testAdd(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 3), 
#             Token(TokenTypes.PLUS, "+"),
#             Token(TokenTypes.INT, 5),
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: int = 8
#         self.assertEqual(first=output, second=expected)
    
#     def testSub(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 3), 
#             Token(TokenTypes.MINUS, "-"),
#             Token(TokenTypes.INT, 5),
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: int = -2
#         self.assertEqual(first=output, second=expected)
    
#     def testMulti(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 3), 
#             Token(TokenTypes.MUL, "*"),
#             Token(TokenTypes.INT, 5),
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: int = 15
#         self.assertEqual(first=output, second=expected)

#     def testDiv(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 6), 
#             Token(TokenTypes.DIV, "/"),
#             Token(TokenTypes.INT, 2),
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: float = 3.0
#         self.assertEqual(first=output, second=expected)

#     def testAssoc(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 9), 
#             Token(TokenTypes.MINUS, "-"),
#             Token(TokenTypes.INT, 5),
#             Token(TokenTypes.PLUS, "+"),
#             Token(TokenTypes.INT, 3),
#             Token(TokenTypes.PLUS, "+"),
#             Token(TokenTypes.INT, 11),
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: int = 9 - 5 + 3 + 11
#         self.assertEqual(first=output, second=expected)
    
#     def testPrecedence(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 7), 
#             Token(TokenTypes.PLUS, "+"),
#             Token(TokenTypes.INT, 5),
#             Token(TokenTypes.MUL, "*"),
#             Token(TokenTypes.INT, 2)
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: int = 7 + 5 * 2
#         self.assertEqual(first=output, second=expected)

#     def testParen(self) -> None:
#         tokens: list[Token] = [
#             Token(TokenTypes.INT, 7), 
#             OPERATORS["+"],
#             Token(TokenTypes.INT, 3),
#             OPERATORS["*"],
#             PARENS["("],
#             Token(TokenTypes.INT, 10),
#             OPERATORS["/"],
#             PARENS["("],
#             Token(TokenTypes.INT, 12),
#             OPERATORS["/"],
#             PARENS["("],
#             Token(TokenTypes.INT, 3),
#             OPERATORS["+"],
#             Token(TokenTypes.INT, 1),
#             PARENS[")"],
#             OPERATORS["-"],
#             Token(TokenTypes.INT, 1),
#             PARENS[")"],
#             PARENS[")"]
#             ]
#         output: int|float = Interpreter.interpret(tokens)
#         expected: float = 7 + 3 * (10 / (12 / (3 + 1) - 1))
#         self.assertEqual(first=output, second=expected)

class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.visitor: Visitor = Visitor()

    def testMalformedOpStart(self) -> None:
        tokens: list[Token] = [
            OPERATORS["*"], 
            Token(TokenTypes.INT, 3)
            ]
        with self.assertRaises(expected_exception=AssertionError):
            Parser(tokens).parse()

    def testMalformedOpMid(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3),
            OPERATORS["*"],
            OPERATORS["/"],
            Token(TokenTypes.INT, 3)
            ]
        with self.assertRaises(expected_exception=AssertionError):
            Parser(tokens).parse()

    def testMalformedOpEnd(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3),
            OPERATORS["*"]
            ]
        with self.assertRaises(expected_exception=AssertionError):
            Parser(tokens).parse()

    def testMalformedNum(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.INT, 3)
            ]
        with self.assertRaises(expected_exception=AssertionError):
            Parser(tokens).parse()

    def testInt(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            ]
        expected: int = 3
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testReal(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.REAL, .123), 
            ]
        expected: float = .123
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testUnary(self) -> None:
        tokens: list[Token] = [
            OPERATORS["+"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 3)
        ]
        expected: int = -3
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testComplexUnary(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 5),
            OPERATORS["-"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 2)
        ]
        expected: int = 7
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testAdd(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 5),
            ]
        expected: int = 8
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testSub(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["-"],
            Token(TokenTypes.INT, 5),
            ]
        expected: int = -2
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testMulti(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["*"],
            Token(TokenTypes.INT, 5),
            ]
        expected: int = 15
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testDiv(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 6), 
            OPERATORS["/"],
            Token(TokenTypes.INT, 2),
            ]
        expected: float = 3.0
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testIntDiv(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 6), 
            OPERATORS["DIV"],
            Token(TokenTypes.INT, 2),
            ]
        expected: int = 3
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testAssoc(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 9), 
            OPERATORS["-"],
            Token(TokenTypes.INT, 5),
            OPERATORS["+"],
            Token(TokenTypes.INT, 3),
            OPERATORS["+"],
            Token(TokenTypes.INT, 11),
            ]
        expected: int = 9 - 5 + 3 + 11
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

    def testPrecedence(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 7), 
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.INT, 5),
            OPERATORS["*"],
            Token(TokenTypes.INT, 2)
            ]
        expected: int = 7 + 5 * 2
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

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
        expected: float = 7 + 3 * (10 / (12 / (3 + 1) - 1))
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=self.visitor.visit(root), second=expected)

class PolishPrinterTests(unittest.TestCase):
    def testNum(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3),
            ]
        expected: str = "3"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)

    def testUnary1(self) -> None:
        tokens: list[Token] = [
            OPERATORS["-"],
            OPERATORS["+"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 3),
        ]
        expected: str = "3"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)

    def testUnary2(self) -> None:
        tokens: list[Token] = [
            OPERATORS["-"],
            OPERATORS["-"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 3),
        ]
        expected: str = "-3"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)

    def testSimplex(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["*"],
            Token(TokenTypes.INT, 5),
            ]
        expected: str = "3 5 *"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)

    def testIntDiv(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["DIV"],
            Token(TokenTypes.INT, 5),
            ]
        expected: str = "3 5 DIV"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)
    
    def testComplex(self) -> None:
        tokens: list[Token] = [
            PARENS["("],
            Token(TokenTypes.INT, 3), 
            OPERATORS["+"],
            Token(TokenTypes.INT, 5),
            PARENS[")"],
            OPERATORS["*"],
            Token(TokenTypes.INT, 2),
            ]
        expected: str = "3 5 + 2 *"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().polish(root), second=expected)

class LispPrinterTests(unittest.TestCase):
    def testNum(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3),
            ]
        expected: str = "3"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().lisp(root), second=expected)

    def testUnary(self) -> None:
        tokens: list[Token] = [
            OPERATORS["-"],
            OPERATORS["+"],
            OPERATORS["-"],
            Token(TokenTypes.INT, 3),
        ]
        expected: str = "(- (+ (- 3)))"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().lisp(root), second=expected)

    def testSimplex(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["*"],
            Token(TokenTypes.INT, 5),
            ]
        expected: str = "(* 3 5)"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().lisp(root), second=expected)

    def testIntDiv(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 3), 
            OPERATORS["DIV"],
            Token(TokenTypes.INT, 5),
            ]
        expected: str = "(DIV 3 5)"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().lisp(root), second=expected)
    
    def testComplex(self) -> None:
        tokens: list[Token] = [
            Token(TokenTypes.INT, 2), 
            OPERATORS["+"],
            Token(TokenTypes.INT, 3),
            OPERATORS["*"],
            Token(TokenTypes.INT, 5),
            ]
        expected: str = "(+ 2 (* 3 5))"
        root: AST = Parser(tokens).parse()
        self.assertEqual(first=Printer().lisp(root), second=expected)
    
if __name__ == "__main__":
    unittest.main()