from seedwork.domain.events import DomainEvent


class NameChanged(DomainEvent):
    new_name: str
