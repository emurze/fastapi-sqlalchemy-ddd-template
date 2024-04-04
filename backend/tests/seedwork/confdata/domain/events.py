from seedwork.domain.events import Event


class NameChanged(Event):
    new_name: str
