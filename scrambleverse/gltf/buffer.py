from ..closable import OnceClosable
from ..memory_reader import MemoryReaderView
from typing import TYPE_CHECKING
from .resource_opener import ResourceOpener, ClosableMemoryReaderView

if TYPE_CHECKING:
    from .gltf import GLTFReader

__all__ = ["Buffers"]


class Buffers(OnceClosable):
    __cache: dict[int, ClosableMemoryReaderView | MemoryReaderView] = {}

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

    def __getitem__(self, index: int) -> MemoryReaderView:
        if index in self.__cache:
            return self.__cache[index]

        buffers = self._gltf_data
        buf = buffers[index]
        if "uri" in buf:
            self.__cache[index] = self.__resource_opener.open_uri(buf["uri"])
        else:
            default_buffer_index = len([x for x in buffers[:index] if "uri" not in x])
            self.__cache[index] = self.__reader._default_buffer(default_buffer_index)
        return self.__cache[index]

    def _close(self):
        for buf in self.__cache.values():
            if isinstance(buf, ClosableMemoryReaderView):
                buf.close()
