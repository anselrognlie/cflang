from cflang.io.file_pushback_byte_stream import FilePushbackByteStream
from cflang.cfasm.token.tokenizer import Tokenizer
from cflang.cfasm.token.token import TokenType
import sys

def safe_index(arr, idx, default):
    if idx >= len(arr):
        return default

    return arr[idx]

s = FilePushbackByteStream(safe_index(sys.argv, 1, "sample_data/cfasm/token/simple.cfasm"))
# while not s.eos():
#     print(s.next())

tr = Tokenizer(s)
done = False
while not done:
    t = tr.next()
    # print(t)
    print(t.type, t.buffer, t.value)

    if t.type == TokenType.END:
        break