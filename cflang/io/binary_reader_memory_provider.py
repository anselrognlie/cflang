from .binary_reader_provider import BinaryReaderProvider

class BinaryReaderMemoryProvider(BinaryReaderProvider):
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read(self):
        b = ''
        if self.pos < len(self.data):
            i = self.data[self.pos]
            b = i.to_bytes(1)
            self.pos += 1

        return b
