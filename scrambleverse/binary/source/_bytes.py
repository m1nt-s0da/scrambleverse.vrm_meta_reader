from ._protocol import BinarySourceReadonly, BinarySourceReadWrite, BinaryWriteData
from ...closable import OnceClosable
from typing import overload

__all__ = ["BinaryBytesSourceReadonly", "BinaryBytesSourceReadWrite"]


class BinaryBytesSourceReadonly(OnceClosable, BinarySourceReadonly):
    @overload
    def __init__(self, data: bytes | bytearray) -> None: ...

    @overload
    def __init__(self, data: memoryview, auto_close: bool = False) -> None: ...

    def __init__(self, data: bytes | bytearray | memoryview, auto_close=False) -> None:
        super().__init__()
        self.__auto_close = auto_close if isinstance(data, memoryview) else True
        self.__data = data if isinstance(data, memoryview) else memoryview(data)

    def __len__(self) -> int:
        return len(self.__data)

    def read(self, offset: int, size: int) -> bytes:
        with self.__data[offset : offset + size] as r:
            return bytes(r)

    def _do_close(self):
        if self.__auto_close:
            self.__data.release()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} size={len(self)} source={hex(id(self.__data))}>"


class BinaryBytesSourceReadWrite(BinaryBytesSourceReadonly, BinarySourceReadWrite):
    @overload
    def __init__(self, data: bytearray) -> None: ...

    @overload
    def __init__(self, data: memoryview, auto_close: bool = False) -> None: ...

    def __init__(self, data: bytearray | memoryview, auto_close=False) -> None:
        assert isinstance(data, (bytearray, memoryview))

        if isinstance(data, memoryview):
            assert not data.readonly
            super().__init__(data, auto_close)
        elif isinstance(data, bytearray):
            super().__init__(data)

    def write(self, offset: int, data: BinaryWriteData) -> None:
        self.__data[offset : offset + len(data)] = data
