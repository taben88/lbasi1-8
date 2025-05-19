from common import Token, TokenTypes

def expect(token: Token, expected_type: TokenTypes) -> Token:
    if token.type == expected_type:
        return token
    else:
        raise AssertionError("Unexpected token encountered!")

def interpret(tokens: list[Token]) -> int|float:
    left: int|float = expect(tokens.pop(0), TokenTypes.INT).value
    while tokens:
        op: int = expect(tokens.pop(0), TokenTypes.OP).value
        right: int = expect(tokens.pop(0), TokenTypes.INT).value
        match op:
            case "+":
                left += right
            case "-":
                left -= right
            case "*":
                left *= right
            case "/":
                left /= right
            case _:
                raise AssertionError
    return left