from typing import TYPE_CHECKING
from .._resource_opener import ResourceOpener
from .._buffer import Buffer, Buffers
from ...binary import BinaryReadonlyView


if TYPE_CHECKING:
    from ._glb import GLBReader

__all__ = ["GLBBuffers", "GLBBuffer"]


class GLBBuffer(Buffer):
    def __init__(self, data: BinaryReadonlyView) -> None:
        self.__data = data

    def open(self) -> BinaryReadonlyView:
        return self.__data


class GLBBuffers(Buffers):
    def __init__(self, reader: "GLBReader", *, resource_opener: ResourceOpener) -> None:
        super().__init__(reader, resource_opener=resource_opener)
        self.__reader = reader

    def __getitem__(self, index: int) -> GLBBuffer | Buffer:
        buffers = self._gltf_data
        buf = buffers[index]

        if "uri" not in buf:
            default_buffer_index = len([x for x in buffers[:index] if "uri" not in x])
            return GLBBuffer(self.__reader.bin_chunks[default_buffer_index])
        else:
            return super()[index]
