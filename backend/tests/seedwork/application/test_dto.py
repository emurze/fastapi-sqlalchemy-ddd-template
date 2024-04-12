from uuid import UUID

import pytest
from pydantic import ValidationError, Field

from seedwork.application.dtos import DTO
from seedwork.domain.services import next_id


class CatDto(DTO):
    id: UUID = Field(default_factory=next_id)
    name: str


@pytest.mark.unit
def test_dto_can_be_initialized() -> None:
    CatDto(name="Bars")


@pytest.mark.unit
def test_dto_has_dynamic_validation() -> None:
    with pytest.raises(ValidationError):
        CatDto(id="melon", name="hello")


@pytest.mark.unit
def test_dto_is_immutable() -> None:
    cat = CatDto(name="hello")
    with pytest.raises(ValidationError):
        cat.name = "hello world"


@pytest.mark.unit
def test_dto_allows_arbitrary_types() -> None:
    class Ref:
        pass

    class Dog(DTO):
        ref: Ref

    assert Dog(ref=Ref())
