import pytest

from shared.tests.shared.conftest import Example


def test_cannot_update_id() -> None:
    example = Example(id=1, name="example")
    with pytest.raises(AssertionError):
        example.update(**{"id": "2", "name": "new example"})


def test_can_update() -> None:
    example = Example(id=1, name="example")
    example.update(**{"name": "new example"})
    assert example.id == 1
    assert example.name == "new example"
