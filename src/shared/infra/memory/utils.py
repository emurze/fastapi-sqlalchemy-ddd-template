import itertools as it
from collections.abc import Iterator
from datetime import datetime


def id_int_gen() -> Iterator[int]:
    return it.count(start=1)


def create_at_gen() -> Iterator[datetime]:
    while True:
        yield datetime.utcnow()
