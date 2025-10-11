from ._protocol import BinaryReaderWriterView
from ._slice import BinaryReaderWriterViewSlice
from ...closable import OnceClosable
from ..source import (
    BinarySourceReadWrite,
    BinaryFileSourceReadWrite,
    BinaryMmapSourceReadWrite,
    BinaryBytesSourceReadWrite,
    BinaryWriteData,
)
from .._bytes_region import BytesRegion
import os
from typing import overload

__all__ = ["BinaryReaderWriter"]


class BinaryReaderWriter(OnceClosable):
    __source: BinarySourceReadWrite

    def __init__(self, source: BinarySourceReadWrite, auto_close=False) -> None:
        super().__init__()
        self.__source = source
        self.__auto_close = auto_close

    @property
    def source(self) -> "BinarySourceReadWrite":
        return self.__source

    def __bytes__(self) -> bytes:
        return self.__source.read(0, len(self))

    def __len__(self) -> int:
        return len(self.__source)

    def __getitem__(self, key: slice) -> "BinaryReaderWriterView":
        return BinaryReaderWriterViewSlice(self, key)

    def __setitem__(self, key: slice, value: BinaryWriteData) -> None:
        indices = self.indices()
        [start, stop, step] = key.indices(indices.size)
        assert step == 1
        assert (stop - start) == len(value)
        self.source.write(indices.offset + start, value)

    def indices(self) -> BytesRegion:
        return BytesRegion(0, len(self))

    def _do_close(self):
        if self.__auto_close:
            self.__source.close()

    @overload
    @classmethod
    def from_bytes(cls, data: bytearray): ...

    @overload
    @classmethod
    def from_bytes(cls, data: memoryview, auto_close=False): ...

    @classmethod
    def from_bytes(cls, data: bytearray | memoryview, auto_close=False):
        if isinstance(data, memoryview):
            return cls(
                BinaryBytesSourceReadWrite(data, auto_close=auto_close), auto_close=True
            )
        else:
            return cls(BinaryBytesSourceReadWrite(data), auto_close=True)

    @classmethod
    def open_file(cls, file_path: str | os.PathLike, *, use_mmap: bool = True):
        if use_mmap:
            return cls(BinaryMmapSourceReadWrite.open(file_path), auto_close=True)
        else:
            return cls(BinaryFileSourceReadWrite.open(file_path), auto_close=True)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} source={self.__source}>"
