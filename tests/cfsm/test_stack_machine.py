from cflang.cfsm.stack_machine import StackMachine
from cflang.io.memory_binary_reader import MemoryBinaryReader

def hex_char_to_dec(hex):
    if '0' <= hex <= '9':
        return ord(hex) - ord('0')

    if 'a' <= hex <= 'f':
        return ord(hex) - ord('a')

    if 'A' <= hex <= 'F':
        return ord(hex) - ord('A')

    raise ValueError

def hex_chars_to_int(hex):
    result = 0
    exp = 0
    for n in range(len(hex) - 1, -1, -1):
        result += hex_char_to_dec(hex[n]) * pow(16, exp)
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

def test_add_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 02000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 5