from typing import TypeVar, Generic

T = TypeVar('T')
class Page(Generic[T]):
    def __init__(self, values: T, offset: int, total: int):
        self.values : T = values
        self.count : int = len(values)
        self.offset : int = offset
        self.total : int = total
