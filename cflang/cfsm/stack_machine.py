from cflang.io.binary_reader import EndOfFileBinaryReader
from .opcode import Opcode
from .bit_ops import top_bit_mask
from .data_size import DWORD
from . import fixed_width_math as fwm
from .flag_result import ZERO, CARRY, OVERFLOW, NEGATIVE, ALL_FLAGS

class InvalidOpcodeError(Exception):
    def __init__(self, opcode, offset):
        super().__init__(f'Invalid opcode [{hex(opcode)}] at location {hex(offset)}')
        self.opcode = opcode
        self.offset = offset

class WrapAroundAdder:
    def __init__(self, range):
        self.range = range

    def add(self, a, b):
        return self._adjust(a + b)

    def sub(self, a, b):
        return self._adjust(a - b)

    def _adjust(self, n):
        if n < 0:
            return n + self.range

        return n % self.range

class StackMachine:
    def __init__(self, reader, mem_size=0x10000, rs_size=0x1000):
        self.reader = reader
        self.mem_size = mem_size
        self.memory = [0] * self.mem_size
        self.reader.read_bytes(self.memory)
        self.pc = 0
        self.rs = mem_size - DWORD
        self.empty_rs = self.rs
        self.ds = self.rs - rs_size
        self.empty_ds = self.ds
        self.stop = False
        self.overflow = False
        self.zero = True
        self.carry = False
        self.negative = False

    def run(self):
        while not self.stop:
            self.tick()

        return self.memory[self.ds]

    def tick(self):
        if self.stop:
            return

        curr_pc = self.pc
        try:
            op = self._read_dword_pc()
            handler = StackMachine.handlers[op]
            handler(self)
        except EndOfFileBinaryReader:
            self.stop = True
        except KeyError:
            raise InvalidOpcodeError(opcode=op, offset=curr_pc)

    def _set_flags(self, overflow=None, zero=None, carry=None, negative=None):
        if overflow is not None:
            self.overflow = overflow

        if zero is not None:
            self.zero = zero

        if carry is not None:
            self.carry = carry

        if negative is not None:
            self.negative = negative

    def _set_flags_for_dword(self, n):
        mask = top_bit_mask(DWORD)
        negative = True if n & mask else False
        zero = not bool(n)
        self._set_flags(negative=negative, zero=zero)

    def _read_dword_pc(self):
        i = self._read_dword_mem(self.pc)
        self.pc += DWORD
        return i

    def _read_dword_mem(self, loc):
        i = int.from_bytes(
            bytearray(self.memory[loc + n] for n in range(DWORD)),
            byteorder="little")
        return i

    def _write_dword_mem(self, loc, n):
        encoded = n.to_bytes(length=DWORD, byteorder="little")
        for n, b in enumerate(encoded):
            self.memory[loc + n] = b

    def _push_dword_reg(self, reg, n):
        addr = getattr(self, reg)
        addr, _ = fwm.sub(DWORD, addr, DWORD)
        setattr(self, reg, addr)
        self._write_dword_mem(addr, n)

    def _pop_dword_reg(self, reg):
        addr = getattr(self, reg)
        n = self._read_dword_mem(addr)
        addr, _ = fwm.add(DWORD, addr, DWORD)
        setattr(self, reg, addr)
        return n

    def _push_dword_ds(self, n):
        self._push_dword_reg('ds', n)

    def _pop_dword_ds(self):
        return self._pop_dword_reg('ds')

    def _push_dword_rs(self, n):
        self._push_dword_reg('rs', n)

    def _pop_dword_rs(self):
        return self._pop_dword_reg('rs')

    def _pushi(self):
        arg = self._read_dword_pc()
        self._push_dword_ds(arg)
        self._set_flags_for_dword(arg)

    def _fetchi(self):
        loc = self._read_dword_pc()
        arg = self._read_dword_mem(loc)
        self._push_dword_ds(arg)
        self._set_flags_for_dword(arg)

    def _storei(self):
        loc = self._read_dword_pc()
        arg = self._pop_dword_ds()
        self._write_dword_mem(loc, arg)
        self._set_flags_for_dword(arg)

    def _torsi(self):
        pass

    def _ofrsi(self):
        pass

    def _addi(self):
        arg2 = self._pop_dword_ds()
        arg1 = self._pop_dword_ds()
        result, flags = fwm.add(DWORD, arg1, arg2)
        self._set_flags(**flags.select(ALL_FLAGS))

        self._push_dword_ds(result)

    def _subi(self):
        arg2 = self._pop_dword_ds()
        arg1 = self._pop_dword_ds()
        result, flags = fwm.sub(DWORD, arg1, arg2)
        self._set_flags(**flags.select(ALL_FLAGS))

        self._push_dword_ds(result)

    def _ret(self):
        if self.rs == self.empty_rs:
            self.stop = True
            return

        self.pc = self._pop_dword_rs()

    def _nop(self):
        pass

    handlers = {
        Opcode.PUSHI: _pushi,
        Opcode.ADDI: _addi,
        Opcode.SUBI: _subi,
        Opcode.RET: _ret,
        Opcode.NOP: _nop,
        Opcode.FCHI: _fetchi,
        Opcode.STRI: _storei,
        Opcode.TORSI: _torsi,
        Opcode.OFRSI: _ofrsi,
    }
