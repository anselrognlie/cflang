def hex_char_to_dec(hex_char):
    if '0' <= hex_char <= '9':
        return ord(hex_char) - ord('0')

    if 'a' <= hex_char <= 'f':
        return ord(hex_char) - ord('a')

    if 'A' <= hex_char <= 'F':
        return ord(hex_char) - ord('A')

    raise ValueError

def hex_chars_to_int(hex_chars):
    result = 0
    exp = 0
    for n in range(len(hex_chars) - 1, -1, -1):
        result += hex_char_to_dec(hex_chars[n]) * pow(16, exp)
        exp += 1

    return result

def hex_str_to_int_array(text):
    data = []
    byte = []
    for n in text:
        if n == ' ':
            continue

        byte.append(n)
        if len(byte) == 2:
            i = hex_chars_to_int(byte)
            data.append(i)
            byte = []

    return data
