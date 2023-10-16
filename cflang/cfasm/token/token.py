from enum import Enum

class TokenType(Enum):
    END = 0
    ERROR = 1
    INTEGER = 2
    STRING = 3
    MINUS = 4
    DOT = 5
    POUND = 6
    ID = 7
    NEWLINE = 8
    LPAREN = 10
    RPAREN = 11
    LBRACKET = 12
    RBRACKET = 13
    PLUS = 18
    COLON = 26
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
