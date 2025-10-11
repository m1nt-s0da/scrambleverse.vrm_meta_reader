from .data import GLTFData
from .buffer import Buffers
from .buffer_view import BufferViews
from ..closable import OnceClosable
from pathlib import Path
import os
from .resource_opener import ResourceOpener
from .image import Images
from abc import ABC, abstractmethod
import json
import io
from .texture import Textures

__all__ = ["GLTFReader"]


def is_outside(base: str | os.PathLike, target: str | os.PathLike) -> bool:
    """
    target が base ディレクトリの外側にあるかどうかを確認する
    """
    target = Path(target).resolve()
    base = Path(base).resolve()

    try:
        target.relative_to(base, walk_up=False)  # 外側だと失敗する
        return False
    except ValueError:
        return True


class GLTFReader(OnceClosable, ABC):
    __buffers: Buffers

    def __init__(
        self,
        *,
        resource_opener: ResourceOpener | None = None,
    ) -> None:
        OnceClosable.__init__(self)

        resource_opener = resource_opener or ResourceOpener()

        self.__buffer_views = BufferViews(self)
        self.__images = Images(self, resource_opener=resource_opener)
        self.__textures = Textures(self)
        self.__resource_opener = resource_opener

    @property
    def _resource_opener(self) -> ResourceOpener:
        return self.__resource_opener

    @property
    @abstractmethod
    def _gltf_data(self) -> GLTFData: ...

    def _do_close(self):
        pass

    @property
    def buffers(self):
        return Buffers(self, resource_opener=self._resource_opener)

    @property
    def buffer_views(self):
        return self.__buffer_views

    @property
    def images(self):
        return self.__images

    @property
    def samplers(self):
        return self._gltf_data.get("samplers", [])

    @property
    def textures(self):
        return self.__textures

    # region openers

    @classmethod
    def from_bytes(
        cls, data: bytes, *, resource_opener: ResourceOpener | None = None
    ) -> "GLTFReader":
        return GLTFReaderImpl(json.loads(data), resource_opener=resource_opener)

    @classmethod
    def from_file(
        cls, file: io.BufferedReader, *, resource_opener: ResourceOpener | None = None
    ) -> "GLTFReader":
        return GLTFReaderImpl(json.load(file), resource_opener=resource_opener)

    @classmethod
    def open_file(
        cls,
        file_path: str | os.PathLike,
        *,
        resource_opener: ResourceOpener | None = None,
    ):
        with open(file_path, "rb") as file:
            return cls.from_file(file, resource_opener=resource_opener)

    # endregion


class GLTFReaderImpl(GLTFReader):
    def __init__(
        self,
        gltf_data: GLTFData,
        *,
        resource_opener: ResourceOpener | None = None,
    ) -> None:
        super().__init__(resource_opener=resource_opener)
        self.__gltf_data = gltf_data

    @property
    def _gltf_data(self) -> GLTFData:
        return self.__gltf_data
