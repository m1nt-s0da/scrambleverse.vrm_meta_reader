from ._protocol import BinaryReadonlyView, BytesRegion
from ..source import BinarySourceReadonly

__all__ = ["BinaryReadonlyViewSlice"]


class BinaryReadonlyViewSlice:
    __parent: BinaryReadonlyView
    __key: slice

    def __init__(self, parent: BinaryReadonlyView, key: slice) -> None:
        assert key.step is None or key.step == 1
        self.__parent = parent
        self.__key = key

    @property
    def source(self) -> BinarySourceReadonly:
        return self.__parent.source

    @property
    def parent(self) -> BinaryReadonlyView:
        return self.__parent

    @property
    def _key(self) -> slice:
        return self.__key

    def indices(self) -> BytesRegion:
        parent_indices = self.__parent.indices()
        [start, stop, step] = self.__key.indices(parent_indices.size)
        assert step == 1
        return parent_indices.inset(start, stop - start)

    def __len__(self) -> int:
        return self.indices().size

    def __bytes__(self) -> bytes:
        indices = self.indices()
        return self.source.read(indices.offset, indices.size)

    def __getitem__(self, key: slice) -> BinaryReadonlyView:
        return BinaryReadonlyViewSlice(self, key)

    def __repr__(self) -> str:
        indices = self.indices()
        return f"<{type(self).__name__} offset={indices.offset} size={indices.size} source={self.source}>"
