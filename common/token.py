from enum import IntEnum, auto
from collections import namedtuple

class TokenTypes(IntEnum):
    NONE = 0
    INT = auto()
    OP = auto()
    PAREN = auto()

Token = namedtuple(typename="Token", field_names=["type", "value"])