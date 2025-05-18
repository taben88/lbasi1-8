from common import Token, TokenTypes

def expect(token: Token, expected_type: TokenTypes) -> Token:
    if token.type == expected_type:
        return token
    else:
        print(expected_type)
        print(token)
        raise AssertionError("Unexpected token encountered!")

def interpret(tokens: list[Token]) -> int:
    left: Token = expect(tokens.pop(0), TokenTypes.INT)
    op: Token = expect(tokens.pop(0), TokenTypes.OP)
    right: Token = expect(tokens.pop(0), TokenTypes.INT)
    match op.value:
        case "+":
            return left.value + right.value
        case "-":
            return left.value - right.value
        case _:
            raise AssertionError
    