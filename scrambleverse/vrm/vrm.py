from ..gltf import GLBReader
from .vrm0_meta import VRM0Meta
from .vrm1_meta import VRM1Meta
from ..gltf import ImageWithMIME
from typing import cast


class VRMReader(GLBReader):
    @property
    def VRM(self):
        return self._gltf_data.get("extensions", {}).get("VRM", None)

    @property
    def VRMC_vrm(self):
        return self._gltf_data.get("extensions", {}).get("VRMC_vrm", None)

    @property
    def vrm0meta(self):
        if self.VRM is not None:
            return VRM0Meta(self.VRM["meta"])
        return None

    @property
    def vrm1meta(self):
        if self.VRMC_vrm is not None:
            return VRM1Meta(self.VRMC_vrm["meta"])
        return None

    @property
    def thumbnail(self):
        if self.vrm0meta is not None:
            texture_id = self.vrm0meta["texture"]
            return cast(ImageWithMIME, self.textures[texture_id].source)
        if self.vrm1meta is not None:
            if "thumbnailImage" not in self.vrm1meta:
                return None
            image_id = self.vrm1meta["thumbnailImage"]
            return cast(ImageWithMIME, self.images[image_id])
        return None
