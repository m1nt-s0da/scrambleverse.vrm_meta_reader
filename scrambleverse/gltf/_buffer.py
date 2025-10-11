from ..binary import BinaryReadonlyView
from typing import TYPE_CHECKING
from ._resource_opener import ResourceOpener, ClosableMemoryReaderView
from typing import Protocol

if TYPE_CHECKING:
    from ._gltf import GLTFReader

__all__ = ["Buffer", "URIBuffer", "Buffers"]


class Buffer(Protocol):
    def open(self) -> ClosableMemoryReaderView | BinaryReadonlyView: ...


class URIBuffer(Buffer):
    def __init__(self, resource_opener: ResourceOpener, uri: str) -> None:
        self.__resource_opener = resource_opener
        self.__uri = uri

    def open(self) -> ClosableMemoryReaderView | BinaryReadonlyView:
        return self.__resource_opener.open_uri(self.__uri)


class Buffers:
    def __init__(
        self,
        reader: "GLTFReader",
        *,
        resource_opener: ResourceOpener,
    ) -> None:
        super().__init__()
        self.__reader = reader
        self.__resource_opener = resource_opener

    @property
    def _gltf_data(self):
        return self.__reader._gltf_data.get("buffers", [])

    def __len__(self) -> int:
        return len(self._gltf_data)

    def __getitem__(self, index: int) -> Buffer:
        buffers = self._gltf_data
        buf = buffers[index]

        if "uri" not in buf:
            raise IndexError("Only buffers with URI are supported")

        return URIBuffer(self.__resource_opener, buf["uri"])
