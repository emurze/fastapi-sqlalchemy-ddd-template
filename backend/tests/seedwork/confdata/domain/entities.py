from dataclasses import dataclass, field

from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.services import uuid_field
from tests.seedwork.confdata.domain import value_objects as vos
from tests.seedwork.confdata.domain.events import NameChanged


@dataclass(kw_only=True)
class Example(AggregateRoot):
    id: vos.ExampleId = uuid_field()
    name: str
    items: list["ExampleItem"] = field(default_factory=list)

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.add_domain_event(NameChanged(new_name=new_name))


@dataclass(kw_only=True)
class ExampleItem(LocalEntity):
    id: vos.ExampleItemId = uuid_field()
    name: str
