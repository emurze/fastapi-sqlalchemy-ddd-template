import pytest

from seedwork.domain.services import next_id
from tests.seedwork.confdata.infra.models import ExampleModel


class TestModelBaseMixin:
    @pytest.mark.unit
    def test_get_fields_success(self) -> None:
        assert [*ExampleModel.get_fields()] == ["id", "name"]

    @pytest.mark.unit
    def test_as_dict(self) -> None:
        example = ExampleModel(id=(example_id := next_id()), name="Example 1")
        assert example.as_dict() == {"id": example_id, "name": "Example 1"}

    @pytest.mark.skip
    @pytest.mark.unit
    def test_update(self) -> None:
        pass