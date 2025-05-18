from enum import Enum, auto
import io
from common import Token, TokenTypes

class Modes(Enum):
    INIT = auto()
    SPACE = auto()
    SINGLE = auto()
    MULTI = auto()

OPERATORS: str = "+-"

def lex(src: io.TextIOBase) -> list[Token]:
    buffer: io.StringIO = io.StringIO()
    multi_token_type = TokenTypes.NONE
    tokens: list[Token] = []
    c: str | None = None
    while c := src.read(1):
        match c:
            case c if c.isspace():
                if multi_token_type:
                    tokens.append(Token(multi_token_type, int(buffer.getvalue())))
                    buffer.close()
                    buffer = io.StringIO()
                    multi_token_type = TokenTypes.NONE
                pass
            case c if c.isdigit():
                if not multi_token_type:
                    multi_token_type = TokenTypes.INT
                buffer.write(c)
            case c if c in OPERATORS:
                if multi_token_type:
                    tokens.append(Token(multi_token_type, int(buffer.getvalue())))
                    buffer.close()
                    buffer = io.StringIO()
                    multi_token_type = TokenTypes.NONE
                tokens.append(Token(TokenTypes.OP, c))
            case _:
                raise AssertionError("Unexpected character encountered!")
    if multi_token_type:
        tokens.append(Token(multi_token_type, int(buffer.getvalue())))
        buffer.close()
    return tokens

if __name__ == "__main__":
    print(lex(io.StringIO("12")))