from typing import Protocol
from .._bytes_region import BytesRegion
from ..source import BinarySourceReadWrite, BinaryWriteData


__all__ = ["BinaryReaderWriterView"]


class BinaryReaderWriterView(Protocol):
    def __bytes__(self) -> bytes: ...

    def __len__(self) -> int: ...

    def __getitem__(self, key: slice) -> "BinaryReaderWriterView": ...

    def __setitem__(self, key: slice, value: BinaryWriteData) -> None: ...

    def indices(self) -> BytesRegion: ...

    @property
    def source(self) -> BinarySourceReadWrite: ...
