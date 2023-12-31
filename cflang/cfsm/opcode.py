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
    PUSHR = 8
    POPR = 9
    DROPI = 10
    ANDI = 11
    ORI = 12
    XORI = 13
    DUPI = 14
    OVERI = 15
    SWAPI = 16
    JMP = 17
    IF = 18
    CALL = 19
    HALT = 20
