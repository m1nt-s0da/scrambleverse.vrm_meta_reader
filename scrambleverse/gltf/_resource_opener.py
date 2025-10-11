from typing import Literal
import os
from pathlib import Path
from ..binary import BinaryReader, BinaryReadonlyView
from typing import Protocol, runtime_checkable
from ..datauri import parse_data_uri

__all__ = ["ResourceOpener", "ClosableMemoryReaderView", "RelativeFileBufferOption"]


RelativeFileBufferOption = Literal[
    "disallow", "allow_descendants", "allow_outside", "allow_absolute"
]


def path_outside(base: str | os.PathLike, target: str | os.PathLike) -> bool:
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


@runtime_checkable
class ClosableMemoryReaderView(BinaryReadonlyView, Protocol):
    def close(self): ...


class ResourceOpener:
    def __init__(
        self,
        relative_file_buffer: RelativeFileBufferOption = "disallow",
        relative_file_location: str | os.PathLike | None = None,
    ) -> None:
        self.__relative_file_buffer = relative_file_buffer
        self.__relative_file_location = Path(relative_file_location or ".")

    def open_uri(self, uri: str) -> ClosableMemoryReaderView | BinaryReadonlyView:
        if ":" in uri and not os.path.isabs(uri):
            if uri.startswith("data:"):
                return self._parse_datauri(uri)
            else:
                return self._fetch(uri)
        else:
            if self.__relative_file_buffer == "disallow":
                raise ValueError("Relative file buffer is disallowed.")

            if self.__relative_file_buffer == "allow_descendants":
                if path_outside(self.__relative_file_location, uri):
                    raise ValueError(
                        "Relative file buffer is outside the base directory."
                    )

            if self.__relative_file_buffer != "allow_absolute":
                if os.path.isabs(uri):
                    raise ValueError("Relative file buffer is absolute path.")

            return self._open_file(uri)

    def _open_file(
        self, path: str | os.PathLike
    ) -> ClosableMemoryReaderView | BinaryReadonlyView:
        return BinaryReader.open_file(path)

    def _parse_datauri(self, uri: str) -> ClosableMemoryReaderView | BinaryReadonlyView:
        return BinaryReader.from_bytes(parse_data_uri(uri).data)

    def _fetch(self, uri: str) -> ClosableMemoryReaderView | BinaryReadonlyView:
        import requests

        response = requests.get(uri)
        response.raise_for_status()
        return BinaryReader.from_bytes(response.content)
