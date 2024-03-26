from dataclasses import dataclass

from seedwork.domain.events import Event


@dataclass(frozen=True, slots=True)
class PostAlreadyExist(Event):
    message: str
