from typing import TypedDict

__all__ = [
    "GLTFData",
    "GLTFBuffer",
    "GLTFBufferView",
    "GLTFImageURI",
    "GLTFImageBufferView",
]


class GLTFBufferRequired(TypedDict):
    byteLength: int


class GLTFBuffer(GLTFBufferRequired, total=False):
    uri: str


class GLTFBufferView(TypedDict):
    buffer: int
    byteOffset: int
    byteLength: int
    byteStride: int
    target: int


class GLTFImageURI(TypedDict):
    uri: str


class GLTFImageBufferView(TypedDict):
    bufferView: int
    mimeType: str


class GLTFSampler(TypedDict):
    magFilter: int
    minFilter: int
    wrapS: int
    wrapT: int


class GLTFTexture(TypedDict):
    sampler: int
    source: int


class GLTFData(TypedDict):
    # asset: dict
    # scenes: list[dict]
    # nodes: list[dict]
    # meshes: list[dict]
    buffers: list[GLTFBuffer]
    bufferViews: list[GLTFBufferView]
    # accessors: list[dict]
    # materials: list[dict]
    images: list[GLTFImageURI | GLTFImageBufferView]
    textures: list[GLTFTexture]
    samplers: list[GLTFSampler]
    # animations: list[dict]
    # skins: list[dict]
    # cameras: list[dict]
    # extensionsUsed: list[str]
    # extensionsRequired: list[str]
