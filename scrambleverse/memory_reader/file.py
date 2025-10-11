import os
from threading import Lock
from contextlib import contextmanager

__all__ = ["MemoryReaderFileSource"]


class MemoryReaderFileSource:
    def __init__(self, filepath: str | os.PathLike) -> None:
        self.__file = open(filepath, "rb")
        self.__filepath = filepath

    @property
    def _filepath(self) -> str | os.PathLike:
        return self.__filepath

    @property
    def _file(self):
        return self.__file

    __seek_lock = Lock()

    @contextmanager
    def _seek(self, offset: int, whence: int):
        with self.__seek_lock:
            pos = self.__file.tell()
            self.__file.seek(offset, whence)
            try:
                yield
            finally:
                self.__file.seek(pos)

    def __len__(self) -> int:
        with self._seek(0, os.SEEK_END):
            return self.__file.tell()

    def read(self, offset: int, size: int) -> bytes:
        with self._seek(offset, os.SEEK_SET):
            return self.__file.read(size)

    def close(self):
        self.__file.flush()
        self.__file.close()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} file={self.__filepath} fileno={self.__file.fileno()}>"
