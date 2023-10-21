from cflang.io.file_binary_reader import EndOfFileBinaryReader
from .opcode import Opcode

class StackMachine:
    def __init__(self, reader):
        self.reader = reader
        self.return_stack = []
        self.data_stack = []
        self.memory = [0] * 0x10000
        self.reader.read_bytes(self.memory)
        self.pc = 0
        self.stop = False

    def run(self):
        while not self.stop:
            self.tick()

        return self.data_stack[-1]

    def tick(self):
        if self.stop:
            return

        try:
            op = self._read_dword()
            handler = StackMachine.handlers[op]
            handler(self)
        except EndOfFileBinaryReader:
            pass

    def _read_dword(self):
        i = int.from_bytes(
            bytearray(self.memory[self.pc + n] for n in range(4)),
            byteorder="little")
        self.pc += 4
        return i

    def _pushi(self):
        arg = self._read_dword()
        self.data_stack.append(arg)

    def _addi(self):
        arg1 = self.data_stack.pop()
        arg2 = self.data_stack.pop()
        result = arg1 + arg2
        self.data_stack.append(result)

    def _ret(self):
        if not self.return_stack:
            self.stop = True
            return

        self.pc = self.return_stack.pop()

    handlers = {
        Opcode.PUSHI.value: _pushi,
        Opcode.ADDI.value: _addi,
        Opcode.RET.value: _ret,
    }
