import os
import mmap
from contextlib import contextmanager
import io
import sys
import json
from .buffer_view import BufferView
from .image import Image
from functools import cached_property

__all__ = ["GLBReader", "GLBJsonChunk"]


if sys.platform == "win32":

    def open_mmap_read(file: io.BufferedReader) -> mmap.mmap:
        return mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)


if sys.platform == "linux":

    def open_mmap_read(file: io.BufferedReader) -> mmap.mmap:
        return mmap.mmap(file.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)


class GLBJsonChunk(dict): ...


class GLBReader:
    def __init__(self, mm: mmap.mmap):
        self.mm = mm

    @property
    def magic(self) -> bytes:
        return self.mm[0:4]

    @property
    def version(self) -> int:
        return int.from_bytes(self.mm[4:8], "little")

    @property
    def length(self) -> int:
        return int.from_bytes(self.mm[8:12], "little")

    def chunks(self):
        offset = 12
        while offset < self.length:
            chunk_length = int.from_bytes(self.mm[offset : offset + 4], "little")
            chunk_type = self.mm[offset + 4 : offset + 8]
            chunk_data_slice = slice(offset + 8, offset + 8 + chunk_length)
            yield chunk_type, chunk_data_slice
            offset += 8 + chunk_length

    __json_chunk: GLBJsonChunk | None = None

    def parse_json_chunk(self):
        if self.__json_chunk is not None:
            return self.__json_chunk

        for chunk_type, chunk_data_slice in self.chunks():
            if chunk_type == b"JSON":
                return GLBJsonChunk(json.loads(self.mm[chunk_data_slice]))
        raise ValueError("No JSON chunk found")

    def __getitem__(self, key: slice) -> bytes:
        return self.mm[key]

    @classmethod
    @contextmanager
    def open(cls, file_path: os.PathLike | str):
        with open(file_path, "rb") as f:
            with open_mmap_read(f) as mm:
                yield cls(mm)

    @cached_property
    def buffer_views(self):
        def gen():
            json = self.parse_json_chunk()
            if "bufferViews" in json:
                for bv in json["bufferViews"]:
                    yield BufferView(self, bv)

        return list(gen())

    @cached_property
    def images(self):
        def gen():
            json = self.parse_json_chunk()
            if "images" in json:
                for img in json["images"]:
                    yield Image(self, img)

        return list(gen())
