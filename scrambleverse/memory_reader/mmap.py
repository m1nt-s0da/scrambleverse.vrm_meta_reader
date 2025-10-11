import sys
import mmap
import os
from .file import MemoryReaderFileSource

__all__ = ["MemoryReaderMmapSource"]

if sys.platform == "win32":

    def open_mmap_read(fileno: int) -> mmap.mmap:
        return mmap.mmap(fileno, 0, access=mmap.ACCESS_READ)


if sys.platform == "linux":

    def open_mmap_read(fileno: int) -> mmap.mmap:
        return mmap.mmap(fileno, 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)


class MemoryReaderMmapSource(MemoryReaderFileSource):
    __mmap: mmap.mmap

    def __init__(self, filepath: str | os.PathLike) -> None:
        super().__init__(filepath)
        self.__mmap = open_mmap_read(self._file.fileno())

    def __len__(self) -> int:
        return self.__mmap.size()

    def read(self, offset: int, size: int) -> bytes:
        return self.__mmap[offset : offset + size]

    def close(self):
        self.__mmap.flush()
        self.__mmap.close()
        super().close()
