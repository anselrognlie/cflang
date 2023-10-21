from cflang.io.file_binary_reader import EndOfFileBinaryReader
from .opcode import Opcode

MAX_INT = 0xffffffff

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
        self.adder = WrapAroundAdder(mem_size)
        self.memory = [0] * self.mem_size
        self.reader.read_bytes(self.memory)
        self.pc = 0
        self.rs = 0
        self.ds = self.adder.sub(self.rs, rs_size)
        self.stop = False
        self.overflow = False

    def run(self):
        while not self.stop:
            self.tick()

        return self.memory[self.ds]

    def tick(self):
        if self.stop:
            return

        try:
            op = self._read_dword_pc()
            handler = StackMachine.handlers[op]
            handler(self)
        except EndOfFileBinaryReader:
            pass

    def _read_dword_pc(self):
        i = self._read_dword_mem(self.pc)
        self.pc += 4
        return i

    def _read_dword_mem(self, loc):
        i = int.from_bytes(
            bytearray(self.memory[loc + n] for n in range(4)),
            byteorder="little")
        return i

    def _write_dword_mem(self, loc, n):
        encoded = n.to_bytes(length=4, byteorder="little")
        for n, b in enumerate(encoded):
            self.memory[loc + n] = b

    def _push_dword_reg(self, reg, n):
        addr = getattr(self, reg)
        addr = self.adder.sub(addr, 4)
        setattr(self, reg, addr)
        self._write_dword_mem(addr, n)

    def _pop_dword_reg(self, reg):
        addr = getattr(self, reg)
        n = self._read_dword_mem(addr)
        addr = self.adder.add(addr, 4)
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

    def _addi(self):
        arg1 = self._pop_dword_ds()
        arg2 = self._pop_dword_ds()
        if MAX_INT - arg1 < arg2:
            self.overflow = True
            result = arg1 - MAX_INT + arg2
        else:
            self.overflow = False
            result = arg1 + arg2

        self._push_dword_ds(result)

    def _ret(self):
        if self.rs == 0:
            self.stop = True
            return

        self.pc = self._pop_dword_rs()

    handlers = {
        Opcode.PUSHI: _pushi,
        Opcode.ADDI: _addi,
        Opcode.RET: _ret,
    }
