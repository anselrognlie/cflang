from collections import deque
from .token import Token, TokenType

class CharTokenizerError(Exception):
    def __init__(self, parsed=None):
        super().__init__()
        self.parsed = parsed

class Tokenizer:
    WHITESPACE = set([' ', '\t'])
    STR_TERM = set(['"', '\n'])
    CHR_TERM = set(["'", '\n'])

    RESERVED = {
    }

    SINGLE_CHAR_TOKENS = {
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        ":": TokenType.COLON,
        ",": TokenType.COMMA,
        "\n": TokenType.NEWLINE,
        "#": TokenType.POUND,
    }

    def __init__(self, stream):
        self.stream = stream
        self.token_buffer = deque()
        self.char_buffer = []
        self.str_buffer = []
        self.location = stream.get_location()

    def next(self):
        if self.eos():
            return Token(
                type=TokenType.END,
                buffer="",
                value=None,
                location=self.location)

        return self.token_buffer.popleft()

    def pushback(self, c):
        self.token_buffer.appendleft(c)

    def eos(self):
        if self.token_buffer:
            return False

        self._prime_buffer()
        return not bool(self.token_buffer)

    def _prime_buffer(self):
        if not self.token_buffer:
            t = self._read_token()
            if t:
                self.token_buffer.append(t)

    # returns: (eos, last_char)
    def _eat(self):
        self.location = self.stream.get_location()
        if self.stream.eos():
            return (True, '')

        done = False
        while not done:
            if self._try_read(";"):
                if self.stream.eos():
                    return (True, '')
                c = self.stream.next()
                while c != "\n":
                    if self.stream.eos():
                        return (True, '')
                    c = self.stream.next()
                self.stream.pushback(c)
                self.location = self.stream.get_location()
                continue

            c = self.stream.next()
            if self._is_whitespace(c):
                self.location = self.stream.get_location()
                if self.stream.eos():
                    return (True, '')
                continue

            done = True


        return (False, c)

    def _error(self, buffer=None):
        if buffer is None:
            buffer = "".join(self.char_buffer)

        return Token(
            type=TokenType.ERROR,
            buffer=buffer,
            value=None,
            location=self.location)

    def _token(self, type, value=None):
        return Token(
            type=type,
            buffer="".join(self.char_buffer),
            value=value,
            location=self.location)

    def _read_token(self):
        eos, c = self._eat()

        if eos:
            return

        self.char_buffer = [c]
        token = self._try_parse_number(c)
        if token is not None:
            return token

        # if self._is_digit(c):
        #     self.char_buffer = [c]
        #     return self._parse_number()
        if self._is_id_start(c):
            return self._parse_id()
        elif c =='"':
            self.str_buffer = []
            return self._parse_string()

        # check single char tokens
        type = Tokenizer.SINGLE_CHAR_TOKENS.get(c, TokenType.ERROR)
        if type != TokenType.ERROR:
            return self._token(type)

        return self._error(c)

    def _is_hex_digit(self, c):
        return ((c >= 'a' and c <= 'f')
                or (c >= 'A' and c <= 'F')
                or self._is_digit(c))

    def _is_digit(self, c):
        return c == '0' or self._is_digit_start(c)

    def _is_digit_start(self, c):
        return c >= '1' and c <= '9'

    def _is_id_start(self, c):
        return ((c >= 'a' and c <= 'z')
                or (c >= 'A' and c <= 'Z')
                or c == "_")

    def _is_id(self, c):
        return self._is_digit(c) or self._is_id_start(c)

    def _is_whitespace(self, c):
        return c in Tokenizer.WHITESPACE

    def _try_read(self, pattern):
        chars = len(pattern)
        rollback = False
        for i in range(chars):
            if self.stream.eos():
                rollback = True
                break  # rollback

            c = self.stream.next()
            self.char_buffer.append(c)
            if c != pattern[i]:
                i += 1
                rollback = True
                break  # rollback

        if rollback:
            while i:
                c = self.char_buffer.pop()
                self.stream.pushback(c)
                i -= 1

        return not rollback

    def _parse_hex(self):
        # must be at least one digit, otherwise error
        if self.stream.eos():
            return self._error()

        c = self.stream.next()
        if not self._is_hex_digit(c):
            self.stream.pushback(c)
            return self._error()

        while self._is_hex_digit(c):
            self.char_buffer.append(c)
            if self.stream.eos():
                break
            c = self.stream.next()

        return self._token(TokenType.INTEGER)

    def _parse_int(self):
        while not self.stream.eos():
            c = self.stream.next()
            if not self._is_digit(c):
                self.stream.pushback(c)
                break

            self.char_buffer.append(c)

        return self._token(TokenType.INTEGER)

    def _try_parse_number(self, c):
        if c == "0":
            # if starts with 0, must either be 0x or 0.
            if self._try_read("x"):
                # hex literal, must be at least one more digit
                return self._parse_hex()
            else:
                # integer 0
                return self._token(TokenType.INTEGER)

        elif self._is_digit(c):
            # integer or float
            return self._parse_int()

        return None

    def _parse_id(self):
        while not self.stream.eos():
            c = self.stream.next()
            if not self._is_id(c):
                self.stream.pushback(c)
                break

            self.char_buffer.append(c)

        type = Tokenizer.RESERVED.get("".join(self.char_buffer), TokenType.ID)
        return self._token(type)

    def _is_str_term(self, c):
        return c in Tokenizer.STR_TERM

    def _parse_string(self):
        while not self.stream.eos():
            c = self.stream.next()
            if self._is_str_term(c):
                if c != '"':
                    self.stream.pushback(c)
                    return self._error()

                self.char_buffer.append(c)
                return self._token(TokenType.STRING, "".join(self.str_buffer))

            self.stream.pushback(c)
            try:
                parsed, value = self._read_char()
                self.char_buffer.extend(parsed)
                self.str_buffer.append(value)
            except CharTokenizerError:
                return self._error()

        return self._error()

    # parsed, value
    def _read_char(self):
        if self.stream.eos():
            raise CharTokenizerError

        c = self.stream.next()
        if c == "\n":
            self.stream.pushback(c)
            raise CharTokenizerError

        return [c], c

