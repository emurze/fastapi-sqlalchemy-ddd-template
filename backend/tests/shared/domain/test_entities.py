import pytest
from pydantic import ValidationError

from shared.application.commands import CommandResult
from shared.domain.errors import Error
from shared.utils.functional import get_const
from tests.shared.conftest_data.domain import Example


@pytest.mark.unit
def test_cannot_update_id() -> None:
    example = Example(name="example")
    with pytest.raises(AssertionError):
        example.update(**{"id": "2", "name": "new example"})


@pytest.mark.unit
def test_can_update() -> None:
    example = Example(name="example")
    example.update(**{"name": "new example"})
    assert example.name == "new example"


@pytest.mark.unit
def test_as_dict_has_no_onw_deferred_field() -> None:
    example = Example(name="example")
    assert example.as_dict() == {"name": "example"}


@pytest.mark.unit
def test_field_metadata() -> None:
    assert get_const(Example.name, "max_length") == 10
