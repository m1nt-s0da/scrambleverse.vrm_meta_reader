from typing import Protocol, NamedTuple


__all__ = ["MemoryReaderView", "MemoryReaderSource", "MemoryReaderRegion"]


class MemoryReaderRegion(NamedTuple):
    offset: int
    size: int

    def inset(self, offset: int, size: int) -> "MemoryReaderRegion":
        assert 0 <= offset <= self.size
        assert 0 <= size <= self.size - offset
        return MemoryReaderRegion(self.offset + offset, size)

    @property
    def slice(self) -> slice:
        return slice(self.offset, self.offset + self.size)


class MemoryReaderSource(Protocol):
    def __len__(self) -> int: ...

    def read(self, offset: int, size: int) -> bytes: ...

    def close(self): ...


class MemoryReaderView(Protocol):
    def __bytes__(self) -> bytes: ...

    def __getitem__(self, key: slice) -> "MemoryReaderView": ...

    def __len__(self) -> int: ...

    def indices(self) -> MemoryReaderRegion: ...

    @property
    def source(self) -> MemoryReaderSource: ...
