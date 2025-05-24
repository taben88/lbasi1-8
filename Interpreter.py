from common import Token, TokenTypes

def expect(tokens: list[Token], expected_type: TokenTypes) -> Token:
    if tokens[0].type == expected_type:
        return tokens.pop(0)
    else:
        raise AssertionError("Unexpected token encountered!")

def operand(tokens: list[Token]) -> int:
    return expect(tokens, TokenTypes.INT).value

def product(tokens: list[Token]) -> int|float:
    result: int|float = operand(tokens)
    while tokens and tokens[0].value in "*/":
        tval: str = expect(tokens, TokenTypes.OP).value
        match tval:
                case "*":
                    result *= operand(tokens)
                case "/":
                    result /= operand(tokens)
                case _:
                    pass
    return result

def sum_(tokens: list[Token]) -> int|float:
    result: int|float = product(tokens)
    while tokens and tokens[0].value in "+-":
        tval: str = expect(tokens, TokenTypes.OP).value
        match tval:
                case "+":
                    result += product(tokens)
                case "-":
                    result -= product(tokens)
                case _:
                    pass
    return result

def interpret(tokens: list[Token]) -> int|float:
    return sum_(tokens)

# def interpret(tokens: list[Token]) -> int|float:
#     left: int|float = expect(tokens.pop(0), TokenTypes.INT).value
#     while tokens:
#         op: int = expect(tokens.pop(0), TokenTypes.OP).value
#         right: int = expect(tokens.pop(0), TokenTypes.INT).value
#         match op:
#             case "+":
#                 left += right
#             case "-":
#                 left -= right
#             case "*":
#                 left *= right
#             case "/":
#                 left /= right
#             case _:
#                 raise AssertionError
#     return left