from common import Token, TokenTypes, OPERATORS, PARENS

def expect(tokens: list[Token], expected_type: TokenTypes) -> Token:
    if tokens[0].type == expected_type:
        return tokens.pop(0)
    else:
        raise AssertionError("Unexpected token encountered!")
    
def integer(tokens: list[Token]) -> int:
    return expect(tokens, TokenTypes.INT).value

def paren(tokens: list[Token]) -> int|float:
    expect(tokens, TokenTypes.LPAREN)
    result = sum_(tokens)
    expect(tokens, TokenTypes.RPAREN)
    return result

def operand(tokens: list[Token]) -> int|float:
    ttype: TokenTypes = tokens[0].type
    out: int|float
    match ttype:
        case TokenTypes.INT:
            out = integer(tokens)
        case TokenTypes.LPAREN:
            out = paren(tokens)
        case _:
            raise AssertionError
    return out

def product(tokens: list[Token]) -> int|float:
    result: int|float = operand(tokens)
    while tokens and tokens[0].type in {TokenTypes.DIV, TokenTypes.MUL}:
        ttype: TokenTypes = tokens[0].type
        expect(tokens, ttype)
        match ttype:
                case TokenTypes.MUL:
                    result *= operand(tokens)
                case TokenTypes.DIV:
                    result /= operand(tokens)
                case _:
                    pass
    return result

def sum_(tokens: list[Token]) -> int|float:
    result: int|float = product(tokens)
    while tokens and tokens[0].type in {TokenTypes.PLUS, TokenTypes.MINUS}:
        ttype: TokenTypes = tokens[0].type
        expect(tokens, ttype)
        match ttype:
                case TokenTypes.PLUS:
                    result += product(tokens)
                case TokenTypes.MINUS:
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

# while token:
#  if paren:
#   result = in_paren()
#  else:
#   result = sum