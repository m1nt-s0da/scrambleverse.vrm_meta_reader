from .protocol import MemoryReaderView, MemoryReaderSource

__all__ = ["MemoryReaderViewSlice"]


class MemoryReaderViewSlice:
    __parent: MemoryReaderView
    __key: slice

    def __init__(self, parent: MemoryReaderView, key: slice) -> None:
        assert key.step is None or key.step == 1
        self.__parent = parent
        self.__key = key

    @property
    def source(self) -> MemoryReaderSource:
        return self.__parent.source

    @property
    def parent(self) -> MemoryReaderView:
        return self.__parent

    @property
    def _key(self) -> slice:
        return self.__key

    def indices(self) -> slice:
        parent_slice = self.__parent.indices()
        assert parent_slice.step is None or parent_slice.step == 1
        parent_slice_length = parent_slice.stop - parent_slice.start
        self_slice = slice(*self.__key.indices(parent_slice_length))
        return slice(
            parent_slice.start + self_slice.start,
            parent_slice.start + self_slice.stop,
        )

    def __len__(self) -> int:
        indices = self.indices()
        return indices.stop - indices.start

    def __bytes__(self) -> bytes:
        indices = self.indices()
        return self.source[indices]

    def __getitem__(self, key: slice) -> MemoryReaderView:
        return MemoryReaderViewSlice(self, key)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.indices()}>"
