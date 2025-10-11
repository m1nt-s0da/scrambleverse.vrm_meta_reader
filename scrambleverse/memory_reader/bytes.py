from typing import overload

__all__ = ["MemoryReaderBytesSource"]


class MemoryReaderBytesSource:
    __data: memoryview
    __auto_close: bool

    @overload
    def __init__(self, data: bytes | bytearray) -> None: ...

    @overload
    def __init__(self, data: memoryview, auto_close: bool = True) -> None: ...

    def __init__(self, data: bytes | bytearray | memoryview, auto_close=True) -> None:
        self.__data = data if isinstance(data, memoryview) else memoryview(data)
        self.__auto_close = auto_close if isinstance(data, memoryview) else True

    def __len__(self) -> int:
        return len(self.__data)

    def read(self, offset: int, size: int) -> bytes:
        with self.__data[offset : offset + size] as r:
            return bytes(r)

    def close(self):
        if self.__auto_close:
            self.__data.release()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} size={len(self.__data)} source={hex(id(self.__data))}>"
