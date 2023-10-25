from cflang.cfsm.stack_machine import StackMachine
from cflang.io.memory_binary_reader import MemoryBinaryReader
from .hex_loader import hex_str_to_int_array
from cflang.cfsm.data_size import DWORD

def get_dword_from_mem(mem, addr):
    data = mem[addr:addr+4]
    return int.from_bytes(bytearray(data), byteorder="little")

def test_push_and_drop():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 0a000000 14000000")
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
       hex_str_to_int_array("01000000 03000000 01000000 02000000 02000000 14000000")
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
       hex_str_to_int_array("01000000 03000000 01000000 02000000 04000000 14000000")
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
       hex_str_to_int_array("01000000 01000000 00000000 14000000")
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
       hex_str_to_int_array(
           """
           01000000 00000000  # pushi 0
           01000000 24000000  # pushi 0x1c
           07000000           # fetchi
           01000000 28000000  # pushi 0x20
           06000000           # storei
           14000000           # halt
           ffffffff           # 0x24
           00000000           # 0x28
           """)
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0
    assert not sm.carry
    assert not sm.zero  # even though the error code is 0, the last data op stored the
    assert not sm.overflow
    assert sm.negative
    assert get_dword_from_mem(sm.memory, 0x28) == 0xffffffff

def test_and_numbers():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 0f0f0f0f 01000000 ffffffff 0b000000 14000000")
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
       hex_str_to_int_array("01000000 ffffffff 01000000 0f0f0f0f 0c000000 14000000")
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
       hex_str_to_int_array("01000000 0f0f0f0f 01000000 ffffffff 0d000000 14000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 0xf0f0f0f0
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert sm.negative

def test_dup_value():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 0e000000 14000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 3
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative
    assert sm.empty_sp - sm.sp == 2 * DWORD

def test_over_value():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 0f000000 14000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 3
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative
    assert sm.empty_sp - sm.sp == 3 * DWORD
    assert get_dword_from_mem(sm.memory, sm.sp) == 3
    assert get_dword_from_mem(sm.memory, sm.sp + DWORD) == 2
    assert get_dword_from_mem(sm.memory, sm.sp + DWORD * 2) == 3

def test_swap_value():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 01000000 02000000 10000000 14000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 3
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative
    assert sm.empty_sp - sm.sp == 2 * DWORD
    assert get_dword_from_mem(sm.memory, sm.sp) == 3
    assert get_dword_from_mem(sm.memory, sm.sp + DWORD) == 2

def test_jmp_instruction():
    reader = MemoryBinaryReader(
       hex_str_to_int_array("01000000 03000000 11000000 18000000 01000000 02000000 14000000")
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 3
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

def test_if_instruction():
    reader = MemoryBinaryReader(
        hex_str_to_int_array(
            """
            01000000 01000000  # push 1
            01000000 03000000 0e000000  # push 3, dup
            12000000 30000000  # if 0->last line (push 2)
            01000000 03000000 04000000 12000000 38000000  # push 3, sub, if 0->last line (ret)
            01000000 02000000 14000000  # push 2, ret
            """)
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 1
    assert not sm.carry
    assert sm.zero
    assert not sm.overflow
    assert not sm.negative


def test_call_instruction():
    reader = MemoryBinaryReader(
        hex_str_to_int_array(
            """
            01000000 01000000  # push 1
            01000000 01000000  # push 1
            01000000 54000000  # push dec
            13000000           # call dec
            01000000 4c000000  # push result 1
            06000000           # store
            01000000 0a000000  # push 1
            01000000 54000000  # push dec
            13000000           # call dec
            01000000 50000000  # push result 2
            06000000           # store to result 2
            14000000  # halt
            f0f0f0f0  # result 1 (4c)
            f0f0f0f0  # result 2 (50)
            # dec routine (54)
            10000000           # swap
            01000000 01000000  # push 1
            04000000           # sub
            10000000           # swap
            03000000           # ret
            """)
    )

    sm = StackMachine(reader)
    result = sm.run()

    assert result == 1
    assert not sm.carry
    assert not sm.zero
    assert not sm.overflow
    assert not sm.negative

    assert get_dword_from_mem(sm.memory, 0x4c) == 0
    assert get_dword_from_mem(sm.memory, 0x50) == 9

def test_reg_ops():
    reader = MemoryBinaryReader(
        hex_str_to_int_array(
            """
            01000000 01000000  # pushi 1
            15000000  # push sp
            16000001  # pop bp
            15000002  # push pc
            14000000  # halt
            """
        )
    )

    sm = StackMachine(reader)
    result = sm.run()

    # assert
    assert result == 20
    assert sm.bp == 0xfff8

# def test_sample():
#     reader = MemoryBinaryReader(
#         hex_str_to_int_array(
#             """
#             """
#         )
#     )

#     sm = StackMachine(reader)
#     result = sm.run()

#     # assert