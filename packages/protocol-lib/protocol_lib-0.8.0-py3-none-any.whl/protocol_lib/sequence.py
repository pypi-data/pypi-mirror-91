from typing import TypeVar, overload

from typing_extensions import Protocol, runtime_checkable

from .iterable import Iterator

__all__ = ["Sequence"]


T = TypeVar("T")


@runtime_checkable
class Sequence(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> Iterator[T]:
        ...

    def __reversed__(self) -> Iterator[T]:
        ...

    def __len__(self) -> int:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "Sequence[T]":
        ...

    def index(self, value: T, start: int = ..., stop: int = ...) -> int:
        ...

    def count(self, value: T) -> int:
        ...
