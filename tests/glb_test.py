from scrambleverse.vrm import GLBReader
import os


def test_open_glb():
    with GLBReader.open(os.environ["TEST_VRM0"]) as glb:
        assert glb.magic == b"glTF"
        assert glb.version == 2
        glb.parse_json_chunk()
