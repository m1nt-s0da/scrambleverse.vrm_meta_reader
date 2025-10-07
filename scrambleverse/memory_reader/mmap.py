import sys
import mmap
import io
import os
from threading import Lock

__all__ = ["MemoryReaderSourceMmap"]

if sys.platform == "win32":

    def open_mmap_read(fileno: int) -> mmap.mmap:
        return mmap.mmap(fileno, 0, access=mmap.ACCESS_READ)


if sys.platform == "linux":

    def open_mmap_read(fileno: int) -> mmap.mmap:
        return mmap.mmap(fileno, 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)


class MemoryReaderSourceMmap:
    __data: mmap.mmap
    __file: int
    __size: int

    def __init__(self, filepath: str | os.PathLike) -> None:
        self.__file = os.open(filepath, os.O_RDONLY)
        self.__data = open_mmap_read(self.__file)
        self.__size = self.__data.size()

    def __len__(self) -> int:
        return self.__size

    def __getitem__(self, key: slice) -> bytes:
        data = self.__data[key]
        return data

    def close(self):
        self.__data.flush()
        self.__data.close()
        os.close(self.__file)
