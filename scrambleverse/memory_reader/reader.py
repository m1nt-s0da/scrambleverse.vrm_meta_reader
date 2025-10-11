from .protocol import MemoryReaderView, MemoryReaderSource, MemoryReaderRegion
from .slice import MemoryReaderViewSlice
from .bytes import MemoryReaderBytesSource
from ..closable import OnceClosable
from .mmap import MemoryReaderMmapSource
from .file import MemoryReaderFileSource
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
        return self.__source.read(0, len(self))

    def __len__(self) -> int:
        return len(self.__source)

    def __getitem__(self, key: slice) -> "MemoryReaderView":
        return MemoryReaderViewSlice(self, key)

    def indices(self) -> MemoryReaderRegion:
        return MemoryReaderRegion(0, len(self))

    def _do_close(self):
        self.__source.close()

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(MemoryReaderBytesSource(data))

    @classmethod
    def open_file(cls, file_path: str | os.PathLike, *, use_mmap: bool = True):
        if use_mmap:
            return cls(MemoryReaderMmapSource(file_path))
        else:
            return cls(MemoryReaderFileSource(file_path))

    def __repr__(self) -> str:
        return f"<{type(self).__name__} source={self.__source}>"
