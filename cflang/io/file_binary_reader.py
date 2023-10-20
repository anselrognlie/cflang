class EndOfFileBinaryReader(Exception):
    pass

class FileBinaryReader:
    def __init__(self, path):
        self.path = path
        self.pos = 1
        self.file = None
        self.buffer = None
        # self.bytes = None

    def read_dword(self):
        byte_data = bytearray([int.from_bytes(self.read_byte()) for _ in range(4)])
        i = int.from_bytes(byte_data, byteorder='little')
        self._prime_buffer()
        return i

    def read_byte(self):
        self._prime_buffer()
        if not self.buffer:
            raise EndOfFileBinaryReader
        b = self.buffer
        self.buffer = None
        self._prime_buffer()
        return b

    def read_bytes(self, into):
        try:
            n = 0
            while b := self.read_byte():
                into[n] = b
                n += 1
        except EndOfFileBinaryReader:
            pass

    def _ensure_open(self):
        if not self.file:
            self.file = open(self.path, 'rb')

    def _prime_buffer(self):
        if not self.buffer:
            self._ensure_open()
            self.buffer = self.file.read(1)
