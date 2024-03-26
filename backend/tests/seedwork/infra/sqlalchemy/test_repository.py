import pytest

from tests.seedwork.confdata.uow import IExampleRepository
from tests.seedwork.infra.memory import test_repository as memory


@pytest.mark.integration
async def test_add_update_example(repo: IExampleRepository) -> None:
    await memory.test_add_update_example(repo)


@pytest.mark.integration
async def test_delete(repo: IExampleRepository) -> None:
    await memory.test_delete(repo)


@pytest.mark.integration
async def test_delete_by_id(repo: IExampleRepository) -> None:
    await memory.test_delete_by_id(repo)


@pytest.mark.integration
async def test_get_by_id(repo: IExampleRepository) -> None:
    await memory.test_get_by_id(repo)


@pytest.mark.integration
async def test_get_by_id_not_found_none_res(repo: IExampleRepository) -> None:
    await memory.test_get_by_id_not_found_none_res(repo)
