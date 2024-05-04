from dataclasses import dataclass, field
from typing import Self
from uuid import UUID

import dacite

from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.services import uuid_field
from tests.seedwork.confdata.domain import value_objects as vos
from tests.seedwork.confdata.domain.events import NameChanged
from tests.seedwork.confdata.domain import rules


@dataclass(kw_only=True)
class Example(AggregateRoot):
    id: vos.ExampleId = uuid_field()
    name: str
    items: list["ExampleItem"] = field(default_factory=list)

    def change_name(self, new_name: str) -> None:
        self.check_rule(
            rules.ExampleNameLengthMustBeGreaterThan5(name=self.name)
        )
        self.name = new_name
        self.add_domain_event(NameChanged(new_name=new_name))

    async def update_item(self, item_id: UUID, **kw) -> None:
        for item in await self.awaitable_attrs.items:
            if item.id == item_id:
                for key, value in kw.items():
                    setattr(item, key, value)
                return

    async def find_item(self, item_id):
        return next(
            item for item in await self.awaitable_attrs.items
            if item.id == item_id
        )

    async def delete_example_item(self, item: 'ExampleItem') -> None:
        (await self.awaitable_attrs.items).remove(item)


@dataclass(kw_only=True)
class ExampleItem(LocalEntity):
    id: vos.ExampleItemId = uuid_field()
    name: str
