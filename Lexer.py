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
                case c if c.isdigit() and self.multi_token_type in {TokenTypes.NONE, TokenTypes.INT, TokenTypes.REAL}:
                    if not self.multi_token_type:
                        self.multi_token_type = TokenTypes.INT
                    self.buffer.write(c)
                case c if c == "." and self.multi_token_type in {TokenTypes.NONE, TokenTypes.INT}:
                    self.multi_token_type = TokenTypes.REAL
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

        value = self.buffer.getvalue()
        match self.multi_token_type:
            case TokenTypes.INT:
                value = int(value)
            case TokenTypes.REAL:
                if value[-1] == "." and len(value) > 1:
                    self.multi_token_type = TokenTypes.INT
                    value = int(value[:-1])
                elif any(c.isdigit() for c in value):
                    value = float(self.buffer.getvalue())
                else:
                    raise AssertionError("Incomplete token!")
        self.tokens.append(Token(self.multi_token_type, value))
        self.buffer.close()
        self.buffer = io.StringIO()
        self.multi_token_type = TokenTypes.NONE

if __name__ == "__main__":
    ...