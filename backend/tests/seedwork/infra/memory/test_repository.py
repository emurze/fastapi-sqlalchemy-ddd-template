import pytest

from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.infra.uow import IExampleRepository


@pytest.mark.unit
async def test_add_update_example(repo: IExampleRepository) -> None:
    example = Example(name="example")
    entity_id = await repo.add(example)
    assert example.id == 1
    assert entity_id == 1


@pytest.mark.unit
async def test_delete(repo: IExampleRepository) -> None:
    example = Example(name="example")
    await repo.add(example)
    await repo.delete(example)
    res = await repo.get_by_id(1)
    assert not res


@pytest.mark.unit
async def test_delete_by_id(repo: IExampleRepository) -> None:
    await repo.add(Example(id=1, name="example"))
    await repo.delete_by_id(entity_id=1)

    res = await repo.get_by_id(1)
    assert not res


@pytest.mark.unit
async def test_get_by_id(repo: IExampleRepository) -> None:
    await repo.add(Example(name="example"))
    res = await repo.get_by_id(1)
    assert res.id == 1
    assert res.name == "example"


@pytest.mark.unit
async def test_get_by_id_not_found_none_res(repo: IExampleRepository) -> None:
    res = await repo.get_by_id(1)
    assert not res
