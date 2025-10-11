from ._data import GLTFBufferView
from ..binary import BinaryReadonlyView, BytesRegion
from typing import TYPE_CHECKING
from ._buffer import Buffer

if TYPE_CHECKING:
    from ._gltf import GLTFReader

__all__ = ["BufferView", "BufferViews"]


class BufferView:
    def __init__(self, buffer: Buffer, region: BytesRegion, target: int | None) -> None:
        self.__buffer = buffer
        self.__region = region
        self.__target = target

    @property
    def buffer(self) -> Buffer:
        return self.__buffer

    @property
    def region(self) -> BytesRegion:
        return self.__region

    @property
    def target(self) -> int | None:
        return self.__target

    def open(self) -> BinaryReadonlyView:
        return self.__buffer.open()[self.__region.slice]


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
            self.__reader.buffers[buf_view["buffer"]],
            BytesRegion(
                offset,
                buf_view["byteLength"],
            ),
            buf_view.get("target", None),
        )
