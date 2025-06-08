from abc import ABC, abstractmethod
from common import Token, TokenTypes

class AST(ABC):
    def __init__(self, token: Token, children: list["AST"]) -> None:
        self.token = token
        self.children = children

    def __str__(self) -> str:
        return str(self.token.value)
    
    @abstractmethod
    def accept(self, visitor: "Visitor") -> int|float:
        ...

class Num(AST):
    def __init__(self, token: Token) -> None:
        super().__init__(token=token, children=[])
    
    def accept(self, visitor: "Visitor") -> int|float:
        return visitor.visitNum(self)

class BinOp(AST):
    def __init__(self, token: Token, left: AST, right: AST) -> None:
        super().__init__(token, children = [left, right])

    def accept(self, visitor: "Visitor") -> int|float:
        return visitor.visitBinOp(self)

class Visitor:
    def visit(self, root: AST) -> int|float:
        return root.accept(self)

    def visitNum(self, num: Num) -> int|float:
        return num.token.value

    def visitBinOp(self, op: BinOp) -> int|float:
        left: int|float = op.children[0].accept(self)
        right: int|float = op.children[1].accept(self)
        result: int|float = 0
        match op.token.type:
            case TokenTypes.PLUS:
                result = left + right
            case TokenTypes.MINUS:
                result = left - right
            case TokenTypes.MUL:
                result = left * right
            case TokenTypes.DIV:
                result = left / right
        return result