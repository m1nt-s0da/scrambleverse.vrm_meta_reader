from typing import Protocol

__all__ = ["BinarySourceReadonly", "BinarySourceReadWrite", "BinaryWriteData"]


class BinarySourceReadonly(Protocol):
    def __len__(self) -> int: ...

    def read(self, offset: int, size: int) -> bytes: ...

    def close(self): ...


class BinaryWriteData(Protocol):
    def __len__(self) -> int: ...

    def __buffer__(self, flags: int) -> memoryview: ...


class BinarySourceReadWrite(BinarySourceReadonly, Protocol):
    def write(self, offset: int, data: BinaryWriteData) -> None: ...
