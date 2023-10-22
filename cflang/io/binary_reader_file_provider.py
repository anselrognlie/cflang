from .binary_reader_provider import BinaryReaderProvider

class BinaryReaderFileProvider(BinaryReaderProvider):
    def __init__(self, path):
        self.path = path
        self.file = None

    def _ensure_open(self):
        if not self.file:
            self.file = open(self.path, 'rb')

    def read(self):
        self._ensure_open()
        return self.file.read(1)
