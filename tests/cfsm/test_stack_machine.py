from cflang.cfsm.stack_machine import StackMachine
from cflang.io.memory_binary_reader import MemoryBinaryReader
from .hex_loader import hex_str_to_int_array

def get_dword_from_mem(mem, addr):
    data = mem[addr:addr+4]
    return int.from_bytes(bytearray(data), byteorder="little")

def test_push_and_drop():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 0a000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 3
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_add_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 02000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 5
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_sub_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 04000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 1
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_nop_in_code():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 01000000 00000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 1
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_fetch_and_store():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 00000000 07000000 1c000000 06000000 20000000 03000000 ffffffff")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0
    assert not sm.carry
    assert not sm.zero  # even though the error code is 0, the last data op stored the
    assert not sm.overflow
    assert sm.negative
    assert get_dword_from_mem(sm.memory, 32) == 0xffffffff

def test_xfer_to_return():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 ffffffff 08000000 09000000 03000000")
    )

    sm = StackMachine(reader)
    sm.tick()  # push
    sm.tick()  # to rs

    assert sm.ds == sm.empty_ds
    assert get_dword_from_mem(sm.memory, sm.rs) == 0xffffffff

    sm.tick()  # from rs

    assert sm.rs == sm.empty_rs
    assert get_dword_from_mem(sm.memory, sm.ds) == 0xffffffff

    result = sm.run()

    assert result == 0xffffffff
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert sm.negative

def test_and_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 0f0f0f0f 01000000 ffffffff 0b000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0x0f0f0f0f
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_or_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 ffffffff 01000000 0f0f0f0f 0b000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0xffffffff
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert sm.negative

def test_xor_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 0f0f0f0f 01000000 ffffffff 0b000000 03000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0xf0f0f0f0
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert sm.negative
