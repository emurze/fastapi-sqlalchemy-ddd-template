import itertools as it
from collections.abc import Iterator


def id_int_gen() -> Iterator[int]:
    return it.count(start=1)
