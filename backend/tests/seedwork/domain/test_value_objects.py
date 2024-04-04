import pytest

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.validators import EmailStr
from seedwork.domain.value_objects import ValueObject


class Address(ValueObject):
    city: str
    country: str


class Entity(AggregateRoot):
    id: int
    email: EmailStr
    address: Address


class TestEmail:
    @pytest.mark.unit
    def test_email_str_and_address_vo(self) -> None:
        entity = Entity(
            id=1,
            email="loza@gmail.com",
            address=Address(city="Lolo", country="Lolo")
        )
        print(entity)
