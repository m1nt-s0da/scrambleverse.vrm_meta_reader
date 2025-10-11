from typing import TYPE_CHECKING, Protocol
from .resource_opener import ResourceOpener
from ..memory_reader import MemoryReaderView
from .buffer_view import BufferView

if TYPE_CHECKING:
    from .gltf import GLTFReader

__all__ = ["Images", "Image", "ImageWithURI", "ImageBufferView"]


class Image(Protocol):
    def open(self) -> MemoryReaderView: ...


class ImageWithURI(Image):
    def __init__(self, *, resource_opener: ResourceOpener, uri: str) -> None:
        super().__init__()
        self.resource_opener = resource_opener
        self.__uri = uri

    @property
    def uri(self) -> str:
        return self.__uri

    def open(self) -> MemoryReaderView:
        return self.resource_opener.open_uri(self.__uri)


class ImageBufferView(Image):
    def __init__(self, *, view: BufferView, mime_type: str) -> None:
        super().__init__()
        self.__view = view
        self.__mime_type = mime_type

    @property
    def mime_type(self) -> str:
        return self.__mime_type

    def open(self) -> MemoryReaderView:
        return self.__view.open()


class Images:
    def __init__(
        self, reader: "GLTFReader", *, resource_opener: ResourceOpener
    ) -> None:
        self.__reader = reader
        self.__resource_opener = resource_opener

    @property
    def _gltf_data(self):
        return self.__reader._gltf_data.get("images", [])

    def __len__(self) -> int:
        return len(self._gltf_data)

    def __getitem__(self, index: int):
        img = self._gltf_data[index]
        if "uri" in img:
            return ImageWithURI(resource_opener=self.__resource_opener, uri=img["uri"])
        elif "bufferView" in img and "mimeType" in img:
            return ImageBufferView(
                view=self.__reader.buffer_views[img["bufferView"]],
                mime_type=img["mimeType"],
            )
        else:
            raise ValueError(f"Invalid image at index {index}")
