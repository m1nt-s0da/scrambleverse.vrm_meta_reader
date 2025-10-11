from ...binary import (
    BinaryReader,
    BinaryReadonlyView,
)
from .._gltf import GLTFReader, ResourceOpener
from .._data import GLTFData
from typing import NamedTuple, Literal, cast
import json
import os
from ._buffer import GLBBuffers

__all__ = ["GLBReader", "GLBHeader", "GLBChunk"]


class GLBHeader(NamedTuple):
    magic: bytes
    version: int
    length: int


class GLBChunk(NamedTuple):
    type: Literal[b"JSON", b"BIN\0"]
    data: BinaryReadonlyView


class GLBReader(GLTFReader):
    def __init__(
        self,
        reader: BinaryReader,
        *,
        resource_opener: ResourceOpener | None = None,
    ) -> None:
        super().__init__(resource_opener=resource_opener)

        self.__file = reader

    @property
    def header(self) -> GLBHeader:
        data = bytes(self.__file[0:12])
        return GLBHeader(
            magic=data[0:4],
            version=int.from_bytes(data[4:8], "little"),
            length=int.from_bytes(data[8:12], "little"),
        )

    @property
    def chunks(self):
        def gen():
            offset = 12
            while offset < self.header.length:
                header = bytes(self.__file[offset : offset + 8])
                chunk_length = int.from_bytes(header[0:4], "little")
                chunk_type = header[4:8]

                chunk_data = self.__file[offset + 8 : offset + 8 + chunk_length]
                yield GLBChunk(cast(Literal[b"JSON", b"BIN\0"], chunk_type), chunk_data)
                offset += 8 + chunk_length

        return list(gen())

    @property
    def __gltf_data(self) -> GLTFData:
        return json.loads(bytes(self.json_chunk))

    @property
    def _gltf_data(self):
        return self.__gltf_data

    @property
    def json_chunk(self):
        for chunk_type, chunk_data in self.chunks:
            if chunk_type == b"JSON":
                return chunk_data
        raise ValueError("No JSON chunk found")

    @property
    def bin_chunks(self):
        return [
            chunk_data
            for chunk_type, chunk_data in self.chunks
            if chunk_type == b"BIN\0"
        ]

    @property
    def buffers(self):
        return GLBBuffers(self, resource_opener=self._resource_opener)

    def _default_buffer(self, index: int):
        return self.bin_chunks[index]

    def _do_close(self):
        super()._do_close()
        self.__file.close()

    # region openers

    @classmethod
    def from_bytes(cls, data: bytes, *, resource_opener: ResourceOpener | None = None):
        return cls(BinaryReader.from_bytes(data), resource_opener=resource_opener)

    @classmethod
    def open_file(
        cls,
        file_path: str | os.PathLike,
        *,
        use_mmap: bool = True,
        resource_opener: ResourceOpener | None = None,
    ):
        return cls(
            BinaryReader.open_file(file_path, use_mmap=use_mmap),
            resource_opener=resource_opener,
        )

    # endregion

    def __repr__(self) -> str:
        return f"<{type(self).__name__} reader={self.__file}>"
