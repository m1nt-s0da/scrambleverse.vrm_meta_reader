from typing import Protocol
from .._bytes_region import BytesRegion
from ..source import BinarySourceReadonly


__all__ = ["BinaryReadonlyView"]


class BinaryReadonlyView(Protocol):
    def __bytes__(self) -> bytes: ...

    def __getitem__(self, key: slice) -> "BinaryReadonlyView": ...

    def __len__(self) -> int: ...

    def indices(self) -> BytesRegion: ...

    @property
    def source(self) -> BinarySourceReadonly: ...
