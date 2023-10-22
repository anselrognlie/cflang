from .binary_reader_memory_provider import BinaryReaderMemoryProvider
from .binary_reader import BinaryReader

def MemoryBinaryReader(data):
    return BinaryReader(BinaryReaderMemoryProvider(data))
