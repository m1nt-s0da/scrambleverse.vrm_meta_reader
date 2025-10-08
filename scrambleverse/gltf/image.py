from typing import TYPE_CHECKING
from ..closable import OnceClosable
from .resource_opener import ResourceOpener, ClosableMemoryReaderView
from ..memory_reader import MemoryReaderView

if TYPE_CHECKING:
    from .gltf import GLTFReader

__all__ = ["Images", "ImageData", "Image", "ImageWithURI", "ImageWithMIME"]


class ImageData:
    def __init__(self, *, data: MemoryReaderView) -> None:
        self.__data = data

    @property
    def data(self) -> MemoryReaderView:
        return self.__data


class ImageWithURI(ImageData):
    def __init__(self, *, data: MemoryReaderView, uri: str) -> None:
        super().__init__(data=data)
        self.__uri = uri

    @property
    def uri(self) -> str:
        return self.__uri


class ImageWithMIME(ImageData):
    def __init__(self, *, data: MemoryReaderView, mime_type: str) -> None:
        super().__init__(data=data)
        self.__mime_type = mime_type

    @property
    def mime_type(self) -> str:
        return self.__mime_type


Image = ImageWithURI | ImageWithMIME


class Images(OnceClosable):
    __cache: dict[int, Image] = {}

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
        if index in self.__cache:
            return self.__cache[index]

        img = self._gltf_data[index]
        if "uri" in img:
            self.__cache[index] = ImageWithURI(
                uri=img["uri"],
                data=self.__resource_opener.open_uri(img["uri"]),
            )
        elif "bufferView" in img and "mimeType" in img:
            buf_view = self.__reader.buffer_views[img["bufferView"]]
            self.__cache[index] = ImageWithMIME(
                mime_type=img["mimeType"],
                data=buf_view.view,
            )
        else:
            raise ValueError(f"Invalid image at index {index}")
        return self.__cache[index]

    def _close(self):
        for img in self.__cache.values():
            if isinstance(img.data, ClosableMemoryReaderView):
                img.data.close()
