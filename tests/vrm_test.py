from scrambleverse.vrm import VRMReader
import os


def test_open_vrm0():
    with VRMReader.open(os.environ["TEST_VRM0"]) as vrm:
        assert vrm.magic == b"glTF"
        assert vrm.version == 2
        json = vrm.parse_json_chunk()
        assert json.VRM is not None
        assert json.VRMC_vrm is None
        assert vrm.thumbnail is not None
        print(vrm.thumbnail.name, vrm.thumbnail.mime_type, len(vrm.thumbnail.bytes()))


def test_open_vrm1():
    with VRMReader.open(os.environ["TEST_VRM1"]) as vrm:
        assert vrm.magic == b"glTF"
        assert vrm.version == 2
        json = vrm.parse_json_chunk()
        assert json.VRM is None
        assert json.VRMC_vrm is not None
        assert vrm.thumbnail is not None
        print(vrm.thumbnail.name, vrm.thumbnail.mime_type, len(vrm.thumbnail.bytes()))
