from typing import TYPE_CHECKING, NamedTuple
from ._data import GLTFSampler
from ._image import Image

if TYPE_CHECKING:
    from ._gltf import GLTFReader

__all__ = ["Texture", "Textures"]


class Texture(NamedTuple):
    source: Image
    sampler: GLTFSampler | None


class Textures:
    def __init__(self, reader: "GLTFReader") -> None:
        self.__reader = reader

    @property
    def _gltf_data(self):
        return self.__reader._gltf_data.get("textures", [])

    def __len__(self) -> int:
        return len(self._gltf_data)

    def __getitem__(self, index: int) -> Texture:
        tex = self._gltf_data[index]
        sampler = tex.get("sampler", None)
        return Texture(
            self.__reader.images[tex["source"]],
            self.__reader.samplers[sampler] if sampler is not None else None,
        )
