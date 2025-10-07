from .data import GLTFBufferView
from ..memory_reader import MemoryReaderView
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from .gltf import GLTFReader

__all__ = ["BufferView", "BufferViews"]


class BufferView(NamedTuple):
    view: MemoryReaderView
    target: int | None


class BufferViews:
    def __init__(self, reader: "GLTFReader") -> None:
        self.__reader = reader

    @property
    def _gltf_data(self):
        return self.__reader._gltf_data.get("bufferViews", [])

    def __len__(self) -> int:
        return len(self._gltf_data)

    def __getitem__(self, index: int):
        buf_view: GLTFBufferView = self._gltf_data[index]
        offset = buf_view.get("byteOffset", 0)
        return BufferView(
            self.__reader.buffers[buf_view["buffer"]][
                offset : offset + buf_view["byteLength"]
            ],
            buf_view.get("target", None),
        )
