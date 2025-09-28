from ..glb import GLBReader, GLBJsonChunk, Image
from .vrm0_meta import VRM0Meta
from .vrm1_meta import VRM1Meta


class VRMJsonChunk(GLBJsonChunk):
    @property
    def VRM(self):
        return self.get("extensions", {}).get("VRM", None)

    @property
    def VRMC_vrm(self):
        return self.get("extensions", {}).get("VRMC_vrm", None)

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


class VRMReader(GLBReader):
    def parse_json_chunk(self) -> VRMJsonChunk:
        return VRMJsonChunk(super().parse_json_chunk())

    @property
    def thumbnail(self) -> Image | None:
        json = self.parse_json_chunk()
        if json.vrm0meta is not None:
            texture_id = json.vrm0meta["texture"]
            image_id = json["textures"][texture_id]["source"]
            return self.images[image_id]
        if json.vrm1meta is not None:
            if "thumbnailImage" not in json.vrm1meta:
                return None
            image_id = json.vrm1meta["thumbnailImage"]
            return self.images[image_id]
        return None
