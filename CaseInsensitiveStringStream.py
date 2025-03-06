from antlr4 import InputStream

class CaseInsensitiveStringStream(InputStream):
    def LA(self, offset):
        val = super().LA(offset)
        if val < 0:
            return val
        return ord(chr(val).upper())