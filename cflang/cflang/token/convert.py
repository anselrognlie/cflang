class ConvertError(Exception):
    pass

def str_to_int(buf):
    MAX_INT = 4294967295
    val = 0
    pow = 1
    for d in reversed(buf):
        inc = int(d) * pow
        if MAX_INT - inc < val:
            raise ConvertError(f"integer too large: {''.join(buf)}")
        val += inc
        pow *= 10

    return val
