from ._protocol import BinarySourceReadonly, BinarySourceReadWrite, BinaryWriteData
import os
from typing import IO, Literal
from threading import Lock
from contextlib import contextmanager

__all__ = ["BinaryFileSourceReadonly", "BinaryFileSourceReadWrite"]


FileOpenMode = Literal["read", "readwrite"]


class BinaryFileSourceReadonly(BinarySourceReadonly):
    def __init__(self, file: IO, auto_close=False) -> None:
        self.__file = file
        self.__auto_close = auto_close

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
        if self.__auto_close:
            self.__file.flush()
            self.__file.close()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} size={len(self)} fileno={self.__file.fileno()} file={self.__file.name}>"

    @classmethod
    def open(cls, filepath: str | os.PathLike):
        return cls(open(filepath, "rb"), auto_close=True)


class BinaryFileSourceReadWrite(BinaryFileSourceReadonly, BinarySourceReadWrite):
    def __init__(self, file: IO, auto_close=False) -> None:
        assert not file.closed
        assert file.writable()
        super().__init__(file, auto_close)

    def write(self, offset: int, data: BinaryWriteData) -> None:
        with self._seek(offset, os.SEEK_SET):
            self._file.write(data)

    @classmethod
    def open(cls, filepath: str | os.PathLike):
        return cls(open(filepath, "r+b"), auto_close=True)

    @classmethod
    def create(cls, filepath: str | os.PathLike, size: int):
        file = open(filepath, "w+b")
        file.truncate(size)
        return cls(file, auto_close=True)
