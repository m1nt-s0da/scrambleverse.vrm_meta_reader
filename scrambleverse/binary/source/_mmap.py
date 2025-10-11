from ._protocol import BinarySourceReadonly, BinarySourceReadWrite, BinaryWriteData
from ...memory_mapped_file import MemoryMappedFile
import os

__all__ = ["BinaryMmapSourceReadonly", "BinaryMmapSourceReadWrite"]


class BinaryMmapSourceReadonly(BinarySourceReadonly):
    def __init__(self, mmap: MemoryMappedFile, auto_close=False) -> None:
        self.__mmap = mmap
        self.__auto_close = auto_close

    def __len__(self) -> int:
        return len(self.__mmap)

    def read(self, offset: int, size: int) -> bytes:
        return self.__mmap[offset : offset + size]

    def close(self):
        if self.__auto_close:
            self.__mmap.close()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} size={len(self)} source={self.__mmap}>"

    @classmethod
    def open(cls, filepath: str | os.PathLike, offset=0, length: int | None = None):
        return cls(
            MemoryMappedFile.open(filepath, offset, length, "read"), auto_close=True
        )


class BinaryMmapSourceReadWrite(BinaryMmapSourceReadonly, BinarySourceReadWrite):
    def __init__(self, mmap: MemoryMappedFile, auto_close=False) -> None:
        assert not mmap.mode == "readwrite"
        super().__init__(mmap, auto_close)

    def write(self, offset: int, data: BinaryWriteData) -> None:
        self.__mmap[offset : offset + len(data)] = data

    @classmethod
    def open(cls, filepath: str | os.PathLike, offset=0, length: int | None = None):
        return cls(
            MemoryMappedFile.open(filepath, offset, length, "readwrite"),
            auto_close=True,
        )

    @classmethod
    def create(cls, filepath: str | os.PathLike, size: int, offset=0):
        return cls(MemoryMappedFile.create(filepath, size, offset), auto_close=True)
