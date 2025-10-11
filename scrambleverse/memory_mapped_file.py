from .closable import OnceClosable
import os
from typing import Literal, IO, Protocol
import sys
import mmap

__all__ = ["MemoryMappedFile", "MemoryMappedFileOpenMode"]


MemoryMappedFileOpenMode = Literal["read", "readwrite"]


class SupportsBuffer(Protocol):
    def __buffer__(self, flags: int) -> memoryview: ...


class MemoryMappedFile(OnceClosable):
    __mode: MemoryMappedFileOpenMode

    def __init__(
        self,
        fd: int | IO,
        offset=0,
        length: int | None = None,
        mode: MemoryMappedFileOpenMode = "read",
        auto_close=False,
    ) -> None:
        """
        Arguments:
            auto_close: If True and fd is a file object, close the file object when closing the MemoryMappedFile. If fd is an integer file descriptor, close it when closing the MemoryMappedFile.
        """
        super().__init__()
        self.__fd = fd
        self.__fileno = fd if isinstance(fd, int) else fd.fileno()
        self.__auto_close = auto_close
        self.__mode = mode

        if sys.platform == "win32":
            self.__mmap = mmap.mmap(
                self.__fileno,
                length if length is not None else 0,
                access=mmap.ACCESS_WRITE if mode == "readwrite" else mmap.ACCESS_READ,
                offset=offset,
            )
        else:
            self.__mmap = mmap.mmap(
                self.__fileno,
                length if length is not None else 0,
                flags=mmap.MAP_SHARED if mode == "readwrite" else mmap.MAP_PRIVATE,
                prot=(
                    mmap.PROT_WRITE | mmap.PROT_READ
                    if mode == "readwrite"
                    else mmap.PROT_READ
                ),
                offset=offset,
            )

    @property
    def mmap(self) -> mmap.mmap:
        return self.__mmap

    @property
    def mode(self) -> MemoryMappedFileOpenMode:
        return self.__mode

    def __getitem__(self, key: slice) -> bytes:
        return self.__mmap[key]

    def __setitem__(self, key: slice, value: SupportsBuffer) -> None:
        if self.__mode != "readwrite":
            raise ValueError("MemoryMappedFile is not opened in readwrite mode.")
        self.__mmap[key] = value

    def __len__(self) -> int:
        return self.__mmap.size()

    def _do_close(self) -> None:
        self.__mmap.flush()
        self.__mmap.close()

        if self.__auto_close:
            if isinstance(self.__fd, int):
                os.close(self.__fd)
            else:
                self.__fd.close()

    @classmethod
    def open(
        cls,
        filepath: str | os.PathLike,
        offset=0,
        length: int | None = None,
        mode: MemoryMappedFileOpenMode = "read",
    ):
        file = open(filepath, "r+b" if mode == "readwrite" else "rb")
        return cls(file, offset, length, mode, auto_close=True)

    @classmethod
    def create(
        cls,
        filepath: str | os.PathLike,
        size: int,
        offset=0,
    ):
        file = open(filepath, "wb")
        file.truncate(size + offset)
        return cls(file, offset, size, "readwrite", auto_close=True)

    def __repr__(self) -> str:
        if isinstance(self.__fd, int):
            return f"<{type(self).__name__} mode={self.mode} fileno={self.__fileno}>"
        else:
            return f"<{type(self).__name__} mode={self.mode} fileno={self.__fileno} file={self.__fd.name}>"
