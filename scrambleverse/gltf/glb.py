from ..memory_reader import (
    MemoryReader,
    MemoryReaderSource,
    MemoryReaderView,
    MemoryReaderSourceBytes,
    MemoryReaderSourceMmap,
)
from .gltf import GLTFReader, ResourceOpener
from .data import GLTFData
from typing import NamedTuple, Literal, cast
from functools import cached_property, cache
import json
import os

__all__ = ["GLBReader", "GLBHeader", "GLBChunk"]


class GLBHeader(NamedTuple):
    magic: bytes
    version: int
    length: int


class GLBChunk(NamedTuple):
    type: Literal[b"JSON", b"BIN\0"]
    data: MemoryReaderView


class GLBReader(GLTFReader):
    def __init__(
        self,
        source: MemoryReaderSource,
        *,
        resource_opener: ResourceOpener | None = None,
    ) -> None:
        GLTFReader.__init__(self, resource_opener=resource_opener)

        self.__file = MemoryReader(source)

    @cached_property
    def header(self) -> GLBHeader:
        return GLBHeader(
            magic=bytes(self.__file[0:4]),
            version=int.from_bytes(self.__file[4:8], "little"),
            length=int.from_bytes(self.__file[8:12], "little"),
        )

    @cached_property
    def chunks(self):
        def gen():
            offset = 12
            while offset < self.header.length:
                chunk_length = int.from_bytes(
                    self.__file[offset : offset + 4], "little"
                )
                chunk_type = bytes(self.__file[offset + 4 : offset + 8])
                chunk_data = self.__file[offset + 8 : offset + 8 + chunk_length]
                yield GLBChunk(cast(Literal[b"JSON", b"BIN\0"], chunk_type), chunk_data)
                offset += 8 + chunk_length

        return list(gen())

    @cached_property
    def __gltf_data(self) -> GLTFData:
        return json.loads(bytes(self.json_chunk))

    @property
    def _gltf_data(self):
        return self.__gltf_data

    @cached_property
    def json_chunk(self):
        for chunk_type, chunk_data in self.chunks:
            if chunk_type == b"JSON":
                return chunk_data
        raise ValueError("No JSON chunk found")

    @cached_property
    def bin_chunks(self):
        return [
            chunk_data
            for chunk_type, chunk_data in self.chunks
            if chunk_type == b"BIN\0"
        ]

    def _default_buffer(self, index: int):
        return self.bin_chunks[index]

    def _close(self):
        GLTFReader._close(self)
        self.__file.close()

    @classmethod
    def from_bytes(
        cls, data: bytes, *, resource_opener: ResourceOpener | None = None
    ) -> "GLBReader":
        return cls(MemoryReaderSourceBytes(data), resource_opener=resource_opener)

    @classmethod
    def open_file(
        cls,
        file_path: str | os.PathLike,
        *,
        resource_opener: ResourceOpener | None = None,
    ):
        return cls(
            MemoryReaderSourceMmap(file_path),
            resource_opener=resource_opener,
        )
