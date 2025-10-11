from scrambleverse.vrm import VRMReader
import os


def test_open_vrm0():
    with VRMReader.open_file(os.environ["TEST_VRM0"]) as vrm:
        assert vrm.header.magic == b"glTF"
        assert vrm.header.version == 2
        assert vrm.vrm0meta is not None
        assert vrm.vrm1meta is None
        assert vrm.thumbnail is not None
