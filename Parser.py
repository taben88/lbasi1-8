from common import AST, Num, BinOp, Token, TokenTypes, OPERATORS, PARENS

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.ast_root = None
    
    @property
    def head(self) -> Token:
        return self.tokens[0]
    
    def expect(self, expected_type: TokenTypes) -> Token:
        if self.tokens[0].type == expected_type:
            return self.tokens.pop(0)
        else:
            raise AssertionError("Unexpected token encountered!")

    def num(self) -> AST:
        return Num(self.expect(TokenTypes.INT))

    def paren(self) -> AST:
        self.expect(TokenTypes.LPAREN)
        out: AST = self.sum_()
        self.expect(TokenTypes.RPAREN)
        return out
    
    def operand(self) -> AST:
        ttype: TokenTypes = self.head.type
        out: AST
        match ttype:
            case TokenTypes.INT:
                out = self.num()
            case TokenTypes.LPAREN:
                out = self.paren()
            case _:
                raise AssertionError
        return out
    
    def product(self) -> AST:
        left: AST = self.operand()
        while self.tokens and self.head.type in {TokenTypes.DIV, TokenTypes.MUL}:
            ttype: TokenTypes = self.head.type
            op: AST = BinOp(token=self.expect(ttype), left=left, right=self.operand())
            left = op
        return left

    def sum_(self) -> AST:
        left: AST = self.product()
        while self.tokens and self.head.type in {TokenTypes.PLUS, TokenTypes.MINUS}:
            ttype: TokenTypes = self.head.type
            op: AST = BinOp(token=self.expect(ttype), left=left, right=self.product())
            left = op
        return left

    def parse(self) -> AST:
        return self.sum_()