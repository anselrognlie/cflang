from .binary_reader_file_provider import BinaryReaderFileProvider
from .binary_reader import BinaryReader

def FileBinaryReader(path):
    return BinaryReader(BinaryReaderFileProvider(path))
