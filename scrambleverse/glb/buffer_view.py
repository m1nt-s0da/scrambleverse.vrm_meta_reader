from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .reader import GLBReader

__all__ = ["BufferView"]


class BufferViewData(TypedDict):
    buffer: int
    byteLength: int
    byteOffset: int
    target: int


class BufferView:
    __data: BufferViewData
    __reader: "GLBReader"

    def __init__(self, reader: "GLBReader", data: BufferViewData):
        self.__reader = reader
        self.__data = data

    def get_buffer(self) -> slice:
        for chunk_type, chunk_data_slice in self.__reader.chunks():
            if chunk_type == b"BIN\0":
                # TODO: Handle multiple buffers
                return chunk_data_slice
        raise ValueError("No BIN chunk found")

    def bytes(self) -> bytes:
        buffer_slice = self.get_buffer()
        start = self.__data.get("byteOffset", 0)
        end = start + self.__data["byteLength"]
        return self.__reader.mm[buffer_slice][start:end]
