import pytest
from pydantic import ValidationError

from tests.shared.confdata.entities import Example


@pytest.mark.unit
def test_cannot_update_id() -> None:
    example = Example(name="example")
    with pytest.raises(AssertionError):
        example.update(**{"id": "2", "name": "new example"})


@pytest.mark.unit
def test_can_update() -> None:
    example = Example(name="example")
    example.update(**{"name": "new"})
    assert example.name == "new"


@pytest.mark.unit
def test_can_revalidate_on_update() -> None:
    example = Example(name="example")
    with pytest.raises(ValidationError):
        example.name = "example 123"


@pytest.mark.unit
def test_as_dict_has_no_onw_deferred_field() -> None:
    example = Example(name="example")
    assert example.as_dict() == {"name": "example"}


@pytest.mark.unit
def test_validation_error() -> None:
    with pytest.raises(ValidationError):
        Example(name="example12345")
