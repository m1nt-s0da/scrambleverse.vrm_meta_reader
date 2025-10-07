from abc import ABC, abstractmethod
from threading import Lock

__all__ = ["OnceClosable"]


class OnceClosable(ABC):
    @abstractmethod
    def _close(self):
        """Close the resource."""
        ...

    __closing: Lock = Lock()
    __closed: bool = False

    @property
    def _closed(self) -> bool:
        return self.__closed

    def close(self):
        closing = False
        with self.__closing:
            if not self.__closed:
                self.__closed = True
                closing = True
        if closing:
            self._close()

    def __enter__(self):
        with self.__closing:
            if self.__closed:
                raise RuntimeError("Cannot enter context with closed resource")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()
