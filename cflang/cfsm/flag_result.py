from dataclasses import dataclass

OVERFLOW = 1
ZERO = 1 << 1
CARRY = 1 << 2
NEGATIVE = 1 << 3
ALL_FLAGS = OVERFLOW | ZERO | CARRY | NEGATIVE
VALUE_FLAGS = ZERO | NEGATIVE

@dataclass
class FlagResult:
    overflow: bool = False
    zero: bool = False
    carry: bool = False
    negative: bool = False

    def select(self, mask):
        result = {}

        if mask & OVERFLOW:
            result["overflow"] = self.overflow

        if mask & ZERO:
            result["zero"] = self.zero

        if mask & CARRY:
            result["carry"] = self.carry

        if mask & NEGATIVE:
            result["negative"] = self.negative

        return result