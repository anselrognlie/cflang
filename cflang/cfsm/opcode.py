from enum import IntEnum

class Opcode(IntEnum):
    NOP = 0
    PUSHI = 1
    ADDI = 2
    RET = 3
    SUBI = 4
    BRK = 5
    STRI = 6
    FCHI = 7
    TORSI = 8
    OFRSI = 9
    DROPI = 10
