import pytest

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
def test_to_dict() -> None:
    example = Example(name="example")
    assert example.to_dict() == {"name": "example"}
