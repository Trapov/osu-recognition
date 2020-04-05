from typing import TypeVar, Generic, List

T = TypeVar('T')


class Page(Generic[T]):
    def __init__(self, values: List[T], offset: int, total: int):
        self.values: List[T] = values
        self.count: int = len(values)
        self.offset: int = offset
        self.total: int = total
