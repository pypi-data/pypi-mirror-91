from typing import Union, Optional


class Reader:
    """
    The Reader is in charge of iterating over the source buffer.

    The buffer is seen as a memoryview (a byte array). The reader
    explicitly takes care of unicode characters (UTF-8 only at the
    moment.
    """

    def __init__(self, src: Union[str, bytes]):
        if isinstance(src, str):
            src = src.encode("utf-8")
        self.src = memoryview(src)
        self.pos = 0
        self._rune_start = 0
        self._rune_end = 0
        self._action_context = {}

    def __getitem__(self, slc: slice):
        return self.src[slc]

    @property
    def _rune(self) -> Optional[memoryview]:
        if self._rune_start != self._rune_end:
            return self.src[self._rune_start:self._rune_end]
        return None

    def next(self) -> Optional[int]:
        try:
            res = self.src[self.pos]
        except IndexError:
            return None
        else:
            self.pos += 1
            return res

    def next_rune(self) -> Optional[memoryview]:
        while True:
            rune = self._rune
            try:
                res = self.src[self.pos]
            except IndexError:
                if rune:
                    self._rune_start = self._rune_end = 0
                    return rune
                else:
                    return None
            else:
                # First check if the msb is one
                if res | 0x7f == 0xff:
                    # check if it's a continuation byte
                    if res & 0xc0 != 0x80:
                        if rune is not None:
                            self._rune_start = self._rune_end = 0
                            return rune
                        self._rune_start = self.pos
                    else:
                        self._rune_end = self.pos
                    self.pos += 1
                else:
                    if rune is not None:
                        self._rune_start = self._rune_end = 0
                        return rune
                    self.pos += 1
                    return self.src[self.pos - 1:self.pos]

    def read(self, n: int = 1) -> Optional[bytes]:
        start = self.pos
        for i in range(n):
            if self.next() is None:
                return None
        return bytes(self.src[start:self.pos])
