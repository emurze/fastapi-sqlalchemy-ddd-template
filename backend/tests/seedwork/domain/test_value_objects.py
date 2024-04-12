from uuid import UUID

import pytest

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.services import UUIDField
from seedwork.domain.validators import EmailStr
from seedwork.domain.value_objects import ValueObject


class Address(ValueObject):
    city: str
    country: str


class Entity(AggregateRoot):
    id: UUID = UUIDField
    email: EmailStr
    address: Address


class TestEmail:
    @pytest.mark.unit
    def test_email_str_and_address_vo(self) -> None:
        entity = Entity(
            email="loza@gmail.com",
            address=Address(city="Lolo", country="Lolo")
        )
        print(entity)
