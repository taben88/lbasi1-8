from common import AST, Num, BinOp, Token, TokenTypes
from typing import Callable

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.ast_root = None
    
    @property
    def head(self) -> Token:

        """Return the first token in the queue."""

        return self.tokens[0]
    
    def expect(self, expected_type: TokenTypes) -> Token:

        """Pop and return the first token, if the token is of expected type. Otherwise raise an AttributeError."""

        if self.tokens[0].type == expected_type:
            return self.tokens.pop(0)
        else:
            raise AssertionError("Unexpected token encountered!")

    def num(self) -> AST:

        """Parse and return a Num from a token of type INT."""

        return Num(self.expect(TokenTypes.INT))

    def paren(self) -> AST:

        """Parse and return a the root of subtree between parentheses."""

        self.expect(TokenTypes.LPAREN)
        out: AST = self.sum_()
        self.expect(TokenTypes.RPAREN)
        return out
    
    def operand(self) -> AST:

        """Parse and return operand (single Num node or root of subtree)."""

        ttype: TokenTypes = self.head.type
        out: AST
        match ttype:
            case TokenTypes.INT:
                out = self.num()
            case TokenTypes.LPAREN:
                out = self.paren()
            case _:
                raise AssertionError("Unexpected token encountered!")
        return out

    def operation(self, op_type: set[TokenTypes], op_start: Callable[[], AST]) -> AST:
        out: AST = op_start()
        while self.tokens and self.head.type in op_type:
            op_token: Token = self.expect(self.head.type)
            try:
                right=op_start()
            except IndexError:
                raise AssertionError("No more tokens left!")
            else:
                out = BinOp(token=op_token, left=out, right=right)
        return out

    def product(self) -> AST:
        return self.operation({TokenTypes.DIV, TokenTypes.MUL}, self.operand)

    def sum_(self) -> AST:
        return self.operation({TokenTypes.PLUS, TokenTypes.MINUS}, self.product)

    def parse(self) -> AST:
        out: AST = self.sum_()
        if self.tokens:
            raise AssertionError("Unexpected token encountered!")
        return out