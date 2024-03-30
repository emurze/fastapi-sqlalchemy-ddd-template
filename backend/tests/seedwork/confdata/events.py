from dataclasses import dataclass

from seedwork.domain.events import Event


@dataclass(frozen=True, slots=True)
class NameChanged(Event):
    new_name:  str
