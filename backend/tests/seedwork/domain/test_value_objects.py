import pytest

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.validators import EmailStr
from seedwork.domain.value_objects import Address


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
            address=Address(
                street="Lolo",
                city="Lolo",
                state="Lolo",
                country="Lolo",
            )
        )
        print(entity)
