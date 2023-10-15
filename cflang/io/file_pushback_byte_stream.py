from .pushback_byte_stream import PushbackByteStream
from .location import Location
from collections import deque

class FilePushbackByteStream(PushbackByteStream):
    def __init__(self, path):
        self.path = path
        self.line_no = 1
        self.pos = 1
        self.file = None
        self.buffer = deque()
        self.line_lens = []

    def next(self):
        self._prime_buffer()
        if not self.buffer:
            return ''

        c = self.buffer.popleft()
        if c == '\n':
            self.line_no += 1
            self.line_lens.append(self.pos)
            self.pos = 1
        else:
            self.pos += 1

        return c

    def pushback(self, c):
        self.buffer.appendleft(c)
        if self.pos == 1:
            self.pos = self.line_lens.pop()
            self.line_no -= 1
        else:
            self.pos -= 1

    def eos(self):
        if self.buffer:
            return False

        self._prime_buffer()
        return not bool(self.buffer)

    def get_location(self):
        return Location(self.path, self.line_no, self.pos)

    def _ensure_open(self):
        if not self.file:
            # self.file = open(self.path, 'r', encoding="utf-8")
            # self.file = open(self.path, 'r', encoding="ascii")
            self.file = open(self.path, 'rb')

    def _prime_buffer(self):
        if not self.buffer:
            self._ensure_open()
            c = self.file.read(1)
            if c:
                d = c.decode(errors="replace")
                d = "?" if d =="�" else d
                self.buffer.append(d)
