from typing import TypedDict, TYPE_CHECKING
from .buffer_view import BufferView

if TYPE_CHECKING:
    from .reader import GLBReader

__all__ = ["Image"]


class ImageData(TypedDict):
    bufferView: int
    mimeType: str
    name: str


class Image(BufferView):
    __data: ImageData

    def __init__(self, reader: "GLBReader", data: ImageData):
        json = reader.parse_json_chunk()
        super().__init__(reader, json["bufferViews"][data["bufferView"]])
        self.__data = data

    @property
    def mime_type(self) -> str:
        return self.__data["mimeType"]

    @property
    def name(self) -> str:
        return self.__data.get("name", "")
