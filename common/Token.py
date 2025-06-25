from enum import IntEnum, auto
from collections import namedtuple

class TokenTypes(IntEnum):
    NONE = 0
    INT = auto()
    REAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    INT_DIV = auto()

Token = namedtuple(typename="Token", field_names=["type", "value"])

OPERATORS: dict[str, Token] = {
    "+": Token(TokenTypes.PLUS, "+"),
    "-": Token(TokenTypes.MINUS, "-"),
    "*": Token(TokenTypes.MUL, "*"),
    "/": Token(TokenTypes.DIV, "/"),
    "DIV": Token(TokenTypes.INT_DIV, "DIV")
}

PARENS: dict[str, Token] = {
    "(" : Token(TokenTypes.LPAREN, "("),
    ")" : Token(TokenTypes.RPAREN, ")")
}