from abc import ABC, abstractmethod
from common import Token, TokenTypes

class AST(ABC):
    def __init__(self, token: Token, children: list["AST"]) -> None:
        self.token = token
        self.children = children

    def __str__(self) -> str:
        return str(self.token.value)
    
    @abstractmethod
    def _accept(self, visitor: "Visitor") -> int|float:
        ...

    @abstractmethod
    def _polish(self, printer: "Printer") -> str:
        ...

    @abstractmethod
    def _lisp(self, printer: "Printer") -> str:
        ...

class Num(AST):
    def __init__(self, token: Token) -> None:
        super().__init__(token=token, children=[])
    
    def _accept(self, visitor: "Visitor") -> int|float:
        return visitor.visit_num(self)
    
    def _polish(self, printer: "Printer") -> str:
        return printer._print_num(self)
    
    def _lisp(self, printer: "Printer") -> str:
        return printer._print_num(self)

class UnOp(AST):
    def __init__(self, token: Token, operand: AST) -> None:
        super().__init__(token, children = [operand])

    def _accept(self, visitor: "Visitor") -> int|float:
        return visitor.visit_un_op(self)
    
    def _polish(self, printer: "Printer") -> str:
        return printer._polish_un_op(self)
    
    def _lisp(self, printer: "Printer") -> str:
        return printer._lisp_un_op(self)

class BinOp(AST):
    def __init__(self, token: Token, left: AST, right: AST) -> None:
        super().__init__(token, children = [left, right])

    def _accept(self, visitor: "Visitor") -> int|float:
        return visitor.visit_bin_op(self)

    def _polish(self, printer: "Printer") -> str:
        return printer._polish_bin_op(self)
    
    def _lisp(self, printer: "Printer") -> str:
        return printer._lisp_bin_op(self)

class Visitor:
    def visit(self, root: AST) -> int|float:
        return root._accept(self)

    def visit_num(self, num: Num) -> int|float:
        return num.token.value

    def visit_un_op(self, op: UnOp) -> int|float:
        operand: int|float = op.children[0]._accept(self)
        if op.token.type is TokenTypes.MINUS:
            operand = -operand
        return operand

    def visit_bin_op(self, op: BinOp) -> int|float:
        left: int|float = op.children[0]._accept(self)
        right: int|float = op.children[1]._accept(self)
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
            case TokenTypes.INT_DIV:
                result = left // right
        return result
    
class Printer:
    def _print_num(self, num: Num) -> str:
        return str(num)

    def _polish_un_op(self, op: UnOp) -> str:
        out: str = op.children[0]._polish(self)
        match op.token.type:
            case TokenTypes.MINUS:
                if out[0] != "-":
                    out = f"-{out}"
                else:
                    out = out[1:]
            case _:
                pass
        return out

    def _polish_bin_op(self, op: BinOp) -> str:
        left: str = op.children[0]._polish(self)
        right: str = op.children[1]._polish(self)
        return f"{left} {right} {str(op)}"
    
    def _lisp_un_op(self, op: UnOp) -> str:
        child : str = op.children[0]._lisp(self)
        return f"({str(op)} {child})"

    def _lisp_bin_op(self, op: BinOp) -> str:
        left: str = op.children[0]._lisp(self)
        right: str = op.children[1]._lisp(self)
        return f"({str(op)} {left} {right})"
    
    def polish(self, root: AST) -> str:

        """Return str with RPN representation of mathematical expression."""

        return root._polish(self)

    def lisp(self, root: AST) -> str:

        """Return str with lisp representation of mathematical expression."""

        return root._lisp(self)
    