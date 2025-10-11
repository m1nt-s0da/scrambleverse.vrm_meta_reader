from typing import NamedTuple

__all__ = ["BytesRegion"]


class BytesRegion(NamedTuple):
    offset: int
    size: int

    def inset(self, offset: int, size: int) -> "BytesRegion":
        assert 0 <= offset <= self.size
        assert 0 <= size <= self.size - offset
        return BytesRegion(self.offset + offset, size)

    @property
    def slice(self) -> slice:
        return slice(self.offset, self.offset + self.size)
