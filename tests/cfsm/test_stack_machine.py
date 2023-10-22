from cflang.cfsm.stack_machine import StackMachine
from cflang.io.memory_binary_reader import MemoryBinaryReader
from .hex_loader import hex_str_to_int_array

def test_add_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 02000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 5
