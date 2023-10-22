class EndOfFileBinaryReader(Exception): pass

class BinaryReader:
    def __init__(self, provider):
        self.pos = 1
        self.buffer = None
        self.provider = provider
        # self.bytes = None

    def read_dword(self):
        byte_data = bytearray(self.read_byte() for _ in range(4))
        i = int.from_bytes(byte_data, byteorder='little')
        self._prime_buffer()
        return i

    def read_byte(self):
        self._prime_buffer()
        if self.buffer is None:
            raise EndOfFileBinaryReader
        b = self.buffer
        self.buffer = None
        return b

    def read_bytes(self, into):
        try:
            buf_len = len(into)
            n = 0
            while n < buf_len:
                b = self.read_byte()
                into[n] = b
                n += 1
        except EndOfFileBinaryReader:
            pass

    def _prime_buffer(self):
        if self.buffer is None:
            b = self.provider.read()
            if len(b) == 0:
                return
            self.buffer = int.from_bytes(b)
