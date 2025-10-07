from scrambleverse.vrm import VRMReader
import os


def test_open_vrm1():
    with VRMReader.open_file(os.environ["TEST_VRM1"]) as vrm:
        assert vrm.header.magic == b"glTF"
        assert vrm.header.version == 2
        assert vrm.VRM is None
        assert vrm.VRMC_vrm is not None
        assert vrm.thumbnail is not None
