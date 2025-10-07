__all__ = ["MemoryReaderSourceBytes"]


class MemoryReaderSourceBytes:
    __data: bytes

    def __init__(self, data: bytes) -> None:
        self.__data = data

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, key: slice) -> bytes:
        return self.__data[key]

    def close(self):
        pass
