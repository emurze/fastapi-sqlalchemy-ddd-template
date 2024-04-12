import pytest
from pydantic import ValidationError

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example, NameChanged


class TestUpdate:
    @pytest.mark.unit
    def test_can_update(self) -> None:
        example = Example(name="example")
        example.update(**{"name": "new"})
        assert example.name == "new"

    @pytest.mark.unit
    def test_cannot_update_id(self) -> None:
        example = Example(name="example")
        with pytest.raises(AssertionError):
            example.update(**{"id": next_id(), "name": "new example"})


class TestValidation:
    @pytest.mark.unit
    def test_can_revalidate_on_update(self) -> None:
        example = Example(name="example")
        with pytest.raises(ValidationError):
            example.name = "example 123"

    @pytest.mark.unit
    def test_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Example(name="example12345")


class TestBusinessMethod:
    @pytest.mark.unit
    def test_change_name_can_give_a_new_name(self) -> None:
        example = Example(name="hello")
        example.change_name("helloo")
        assert example.name == "helloo"

    @pytest.mark.unit
    def test_change_name_can_register_only_one_event(self) -> None:
        example = Example(name="hello")
        example.change_name("helloo")
        assert len(example._events) == 1
        assert example._events[0] == NameChanged(new_name="helloo")


class TestAggregateRoot:
    @pytest.mark.unit
    def test_register_event_can_register_only_one_event_at_time(self) -> None:
        example = Example(name="hello")
        example.register_event(NameChanged(new_name="helloo"))
        assert len(example._events) == 1
        assert example._events[0] == NameChanged(new_name="helloo")

    @pytest.mark.unit
    def test_collect_events_dont_duplicate_events(self) -> None:
        example = Example(name="hello")
        example.register_event(NameChanged(new_name="helloo"))
        events = example.collect_events()
        assert len(events) == 1
        assert events[0] == NameChanged(new_name="helloo")

    @pytest.mark.unit
    def test_collect_events_can_clean_events_after_collecting(self) -> None:
        example = Example(name="hello")
        example.register_event(NameChanged(new_name="helloo"))
        example.collect_events()
        assert len(example._events) == 0


class TestCommon:
    @pytest.mark.unit
    def test_c_can_retrieve_field_constraint(self) -> None:
        assert Example.c.name.max_length == 10

    @pytest.mark.unit
    def test_str_can_show_beautiful_representation(self) -> None:
        example = Example(id=(example_id := next_id()), name="example")
        assert str(example) == f"Example(id={example_id}, name='example')"
