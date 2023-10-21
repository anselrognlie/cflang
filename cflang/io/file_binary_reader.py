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

    def _ensure_open(self):
        if not self.file:
            self.file = open(self.path, 'rb')

    def _prime_buffer(self):
        if self.buffer is None:
            self._ensure_open()
            b = self.file.read(1)
            if len(b) == 0:
                return
            self.buffer = int.from_bytes(b)
