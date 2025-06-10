import io
from common import Token, TokenTypes, OPERATORS, PARENS


class Lexer:
    def __init__(self, src: io.TextIOBase) -> None:
        self.src = src # The source code to be lexed
        self.buffer: io.StringIO = io.StringIO() # Buffer to handle items spanning multiple chars
        self.multi_token_type: TokenTypes = TokenTypes.NONE # The type of the multichar token being lexed
        self.tokens: list[Token] = [] # Tokens lexed from source code
    
    def lex(self) -> list[Token]:

        """
            Lex the the content of source, return list of tokens lexed.
        """

        while c := self.src.read(1):
            match c:
                case c if c.isspace():
                    if self.multi_token_type:
                        self._emit_multi()
                    pass
                case c if c.isdigit():
                    if not self.multi_token_type:
                        self.multi_token_type = TokenTypes.INT
                    self.buffer.write(c)
                case c if c in OPERATORS:
                    if self.multi_token_type:
                        self._emit_multi()
                    self.tokens.append(OPERATORS[c])
                case c if c in PARENS:
                    if self.multi_token_type:
                        self._emit_multi()
                    self.tokens.append(PARENS[c])
                case _:
                    raise AssertionError("Unexpected character encountered!")
        if self.multi_token_type:
            self._emit_multi()
        return self.tokens
                
    def _emit_multi(self) -> None:

        """
            Helper function to handle tokens made up of more than one characters.
        """

        match self.multi_token_type:
            case TokenTypes.INT:
                value = int(self.buffer.getvalue())
        self.tokens.append(Token(self.multi_token_type, value))
        self.buffer.close()
        self.buffer = io.StringIO()
        self.multi_token_type = TokenTypes.NONE

if __name__ == "__main__":
    ...