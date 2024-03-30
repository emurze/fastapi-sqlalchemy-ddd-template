from dataclasses import dataclass

import pytest

from seedwork.application.dtos import DTO


@dataclass(frozen=True, slots=True)
class CatDto(DTO):
    id: int
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CatWithNoneDto(DTO):
    id: int | None = None
    name: str


@pytest.mark.unit
def test_as_dict_can_create_dict() -> None:
    cat_dto = CatDto(id=1, name="Bobby")
    assert cat_dto.as_dict() == {"id": 1, "name": "Bobby"}


@pytest.mark.unit
def test_as_dict_can_miss_none_values_by_default() -> None:
    cat_dto = CatWithNoneDto(name="Bobby")
    assert cat_dto.as_dict() == {"name": "Bobby"}


@pytest.mark.unit
def test_as_dict_cannot_miss_none_values() -> None:
    cat_dto = CatWithNoneDto(name="Bobby")
    assert cat_dto.as_dict(exclude_none=True) == {"name": "Bobby"}


@pytest.mark.unit
def test_as_dict_can_exclude_keys() -> None:
    cat_dto = CatDto(id=1, name="Bobby")
    assert cat_dto.as_dict(exclude={"name"}) == {"id": 1}


@pytest.mark.unit
def test_from_model_can_create_dto() -> None:
    cat_dto = CatDto(id=1, name="Bobby")
    new_cat_dto = CatDto.from_model(cat_dto)
    assert new_cat_dto.as_dict() == {"id": 1, "name": "Bobby"}
