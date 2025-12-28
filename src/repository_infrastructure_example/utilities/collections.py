from typing import Sequence, TypeVar

T = TypeVar("T")


def first_element(items: Sequence[T], /) -> T:
    return items[0]
