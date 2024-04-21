import pytest
from pydantic import ValidationError

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example, NameChanged


class TestEntity:
    @pytest.mark.unit
    def test_can_update(self) -> None:
        example = Example(name="example")
        example.update(**{"name": "new"})
        assert example.name == "new"

    @pytest.mark.unit
    def test_can_set_and_get_extra_kw(self) -> None:
        example = Example(name="example")
        example.extra_kw['vlados'] = 'In love'
        assert example.extra_kw['vlados'] == 'In love'

    @pytest.mark.unit
    @pytest.mark.skip
    def test_can_return_only_loaded_relations_as_dict(self) -> None:
        ...

    @pytest.mark.unit
    def test_cannot_update_id(self) -> None:
        example = Example(name="example")
        with pytest.raises(AssertionError):
            example.update(**{"id": next_id(), "name": "new example"})

    @pytest.mark.unit
    def test_can_revalidate_on_update(self) -> None:
        example = Example(name="example")
        with pytest.raises(ValidationError):
            example.name = "example 123"

    @pytest.mark.unit
    def test_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Example(name="example12345")

    @pytest.mark.unit
    def test_change_name_can_give_a_new_name(self) -> None:
        example = Example(name="hello")
        example.change_name("helloo")
        assert example.name == "helloo"

    @pytest.mark.unit
    def test_change_name_can_add_only_one_domain_event(self) -> None:
        example = Example(name="hello")
        example.change_name("helloo")
        assert len(example._events) == 1
        assert example._events[0] == NameChanged(new_name="helloo")

    @pytest.mark.unit
    def test_c_can_retrieve_field_constraint(self) -> None:
        assert Example.c.name.max_length == 10


class TestAggregateRoot:
    @pytest.mark.unit
    def test_can_add_only_one_domain_event_at_time(self) -> None:
        example = Example(name="hello")
        example.add_domain_event(NameChanged(new_name="helloo"))
        assert len(example._events) == 1
        assert example._events[0] == NameChanged(new_name="helloo")

    @pytest.mark.unit
    def test_collect_events_dont_duplicate_events(self) -> None:
        example = Example(name="hello")
        example.add_domain_event(NameChanged(new_name="helloo"))
        events = example.collect_events()
        assert len(events) == 1
        assert events[0] == NameChanged(new_name="helloo")

    @pytest.mark.unit
    def test_collect_events_can_clean_events_after_collecting(self) -> None:
        example = Example(name="hello")
        example.add_domain_event(NameChanged(new_name="helloo"))
        example.collect_events()
        assert len(example._events) == 0
