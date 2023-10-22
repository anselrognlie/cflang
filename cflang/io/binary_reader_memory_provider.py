from .binary_reader_provider import BinaryReaderProvider

class BinaryReaderMemoryProvider(BinaryReaderProvider):
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read(self):
        b = ''
        if self.pos >= len(self.data):
            b = self.data[self.pos]
            self.pos += 1

        return b
