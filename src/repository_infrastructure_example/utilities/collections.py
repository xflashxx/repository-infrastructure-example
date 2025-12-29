from typing import Sequence, TypeVar

T = TypeVar("T")


def first_element(items: Sequence[T], /) -> T:
    """
    Returns the first element of a sequence.

    :param items: The sequence to get the first element from.
    :return: The first element of the sequence.
    :raises IndexError: If the sequence is empty.
    """
    return items[0]
