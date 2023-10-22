from .bit_ops import top_bit_mask
from .flag_result import FlagResult

def add(size, n1, n2):
    max_usgn = 1 << size * 8

    carry = False
    if max_usgn - n1 <= n2:
        result = n1 - max_usgn + n2
        carry = True
    else:
        result = n1 + n2

    mask = top_bit_mask(size)
    overflow = True if not n1 & mask and not n2 & mask and result & mask else False
    negative = True if result & mask else False
    zero = not bool(result)

    return result, FlagResult(zero=zero, negative=negative, carry=carry, overflow=overflow)

def sub(size, n1, n2):
    max_usgn = 1 << size * 8

    carry = False
    if n1 < n2:
        carry = True
        result = max_usgn - n2 + n1
    else:
        result = n1 - n2

    mask = top_bit_mask(size)
    overflow = True if n1 & mask and not n2 & mask and not result & mask else False
    negative = True if result & mask else False
    zero = not bool(result)

    return result, FlagResult(zero=zero, negative=negative, carry=carry, overflow=overflow)


