def make_mask(n):
    return 1 << n

def top_bit_mask(size):
    return make_mask((8 * size) - 1)
