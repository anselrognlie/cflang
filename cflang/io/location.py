class Location:
    def __init__(self, source, line_no, pos):
        self.source = source
        self.line_no = line_no
        self.pos = pos

    def __repr__(self):
        return ("Location("
                f"source={repr(self.source)}, "
                f"line_no={repr(self.line_no)}, "
                f"pos={repr(self.pos)})")