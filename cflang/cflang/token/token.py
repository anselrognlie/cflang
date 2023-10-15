from enum import Enum

class TokenType(Enum):
    END = 0
    ERROR = 1
    INTEGER = 2
    STRING = 3
    MINUS = 4
    DOT = 5
    CHAR = 6
    ID = 7
    TRUE = 8
    FALSE = 9
    LPAREN = 10
    RPAREN = 11
    LBRACKET = 12
    RBRACKET = 13
    LBRACE = 14
    RBRACE = 15
    LT = 16
    GT = 17
    PLUS = 18
    DIV = 19
    MULT = 20
    MOD = 21
    NOT = 22
    EQUAL = 23
    SEMI = 24
    QUESTION = 25
    COLON = 26
    LTE = 27
    GTE = 28
    DBLEQL = 29
    NOTEQL = 30
    PLUSEQL = 31
    MINUSEQL = 32
    MULTEQL = 33
    DIVEQL = 34
    ARROW = 35
    FLOAT = 36
    COMMA = 37

class Token:
    def __init__(self, type, buffer, value, location):
        self.type = type
        self.buffer = buffer
        self.value = value
        self.location = location

    def __repr__(self):
        return (f"Token(type={self.type}, "
            f"buffer={repr(self.buffer)}, "
            f"value={repr(self.value)}, "
            f"location={repr(self.location)})")
