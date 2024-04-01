import pytest
from pydantic import ValidationError

from seedwork.application.dtos import DTO


class CatDto(DTO):
    id: int
    name: str


@pytest.mark.unit
def test_dto_can_be_initialized() -> None:
    CatDto(id=100, name="Bars")


@pytest.mark.unit
def test_dto_has_dynamic_validation() -> None:
    with pytest.raises(ValidationError):
        CatDto(id="melon", name="hello")


@pytest.mark.unit
def test_dto_is_immutable() -> None:
    cat = CatDto(id=1, name="hello")
    with pytest.raises(ValidationError):
        cat.name = "hello world"


@pytest.mark.unit
def test_dto_allows_arbitrary_types() -> None:
    class Ref:
        pass

    class Dog(DTO):
        ref: Ref

    assert Dog(ref=Ref())
