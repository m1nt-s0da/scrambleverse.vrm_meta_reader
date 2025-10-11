from ._protocol import BinaryReadonlyView
from ._slice import BinaryReadonlyViewSlice
from ...closable import OnceClosable
from ..source import (
    BinarySourceReadonly,
    BinaryFileSourceReadonly,
    BinaryMmapSourceReadonly,
    BinaryBytesSourceReadonly,
)
from .._bytes_region import BytesRegion
import os
from typing import overload

__all__ = ["BinaryReader"]


class BinaryReader(OnceClosable):
    __source: BinarySourceReadonly

    def __init__(self, source: BinarySourceReadonly, auto_close=False) -> None:
        super().__init__()
        self.__source = source
        self.__auto_close = auto_close

    @property
    def source(self) -> "BinarySourceReadonly":
        return self.__source

    def __bytes__(self) -> bytes:
        return self.__source.read(0, len(self))

    def __len__(self) -> int:
        return len(self.__source)

    def __getitem__(self, key: slice) -> "BinaryReadonlyView":
        return BinaryReadonlyViewSlice(self, key)

    def indices(self) -> BytesRegion:
        return BytesRegion(0, len(self))

    def _do_close(self):
        if self.__auto_close:
            self.__source.close()

    @overload
    @classmethod
    def from_bytes(cls, data: bytes | bytearray): ...

    @overload
    @classmethod
    def from_bytes(cls, data: memoryview, auto_close=False): ...

    @classmethod
    def from_bytes(cls, data: bytes | bytearray | memoryview, auto_close=False):
        if isinstance(data, memoryview):
            return cls(BinaryBytesSourceReadonly(data, auto_close=auto_close))
        else:
            return cls(BinaryBytesSourceReadonly(data))

    @classmethod
    def open_file(cls, file_path: str | os.PathLike, *, use_mmap: bool = True):
        if use_mmap:
            return cls(BinaryMmapSourceReadonly.open(file_path))
        else:
            return cls(BinaryFileSourceReadonly.open(file_path))

    def __repr__(self) -> str:
        return f"<{type(self).__name__} source={self.__source}>"
