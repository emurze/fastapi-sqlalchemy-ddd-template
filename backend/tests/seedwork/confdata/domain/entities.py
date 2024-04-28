from pydantic import Field

from seedwork.domain.structs import alist
from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.services import UUIDField
from tests.seedwork.confdata.domain import value_objects as vos
from tests.seedwork.confdata.domain.events import NameChanged


class Example(AggregateRoot):
    id: vos.ExampleId = UUIDField
    name: str = Field(max_length=10)
    items: alist["ExampleItem"] = alist()

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.add_domain_event(NameChanged(new_name=new_name))


class ExampleItem(LocalEntity):
    id: vos.ExampleItemId = UUIDField
    name: str
    addresses: alist[vos.Address] = alist()


class Post(AggregateRoot):
    id: vos.PostId = UUIDField
    title: str
    users: alist["User"] = alist()


class User(LocalEntity):
    id: vos.UserId = UUIDField
    name: str
    permissions: alist['Permission'] = alist()


class Permission(LocalEntity):
    id: vos.PermissionId = UUIDField
    name: str
