from .protocol import MemoryReaderView, MemoryReaderSource
from .slice import MemoryReaderViewSlice
from .bytes import MemoryReaderSourceBytes
from ..closable import OnceClosable
from .mmap import MemoryReaderSourceMmap
import os

__all__ = ["MemoryReader"]


class MemoryReader(OnceClosable):
    __source: MemoryReaderSource

    def __init__(self, source: MemoryReaderSource) -> None:
        super().__init__()
        self.__source = source

    @property
    def source(self) -> "MemoryReaderSource":
        return self.__source

    def __bytes__(self) -> bytes:
        return self.__source[:]

    def __len__(self) -> int:
        return len(self.__source)

    def __getitem__(self, key: slice) -> "MemoryReaderView":
        return MemoryReaderViewSlice(self, key)

    def indices(self) -> slice:
        return slice(*slice(None).indices(len(self)))

    def _close(self):
        self.__source.close()

    @classmethod
    def from_bytes(cls, data: bytes) -> "MemoryReader":
        return cls(MemoryReaderSourceBytes(data))

    @classmethod
    def open_file(cls, file_path: str | os.PathLike):
        return cls(MemoryReaderSourceMmap(file_path))
