import pytest

from tests.seedwork.confdata.domain.entities import Example, NameChanged


class TestEntity:
    @pytest.mark.unit
    def test_can_update(self) -> None:
        example = Example(name="example")
        example.update(**{"name": "new"})
        assert example.name == "new"

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


class TestAggregateRoot:
    @pytest.mark.unit
    def test_can_add_only_one_domain_event_at_time(self) -> None:
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
