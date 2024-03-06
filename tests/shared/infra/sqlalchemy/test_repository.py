import pytest

from tests.shared.conftest import IExampleRepository
from tests.shared.infra.memory import test_repository as memory_impl


@pytest.mark.integration
async def test_can_add_and_get(repo: IExampleRepository) -> None:
    await memory_impl.test_can_add_and_get(repo)


@pytest.mark.integration
async def test_get_not_found_error(repo: IExampleRepository) -> None:
    await memory_impl.test_get_not_found_error(repo)


@pytest.mark.integration
async def test_can_get_for_update(repo: IExampleRepository) -> None:
    await memory_impl.test_can_get_for_update(repo)


@pytest.mark.integration
async def test_get_for_update_not_found_error(
    repo: IExampleRepository,
) -> None:
    await memory_impl.test_get_for_update_not_found_error(repo)


@pytest.mark.integration
async def test_list(repo: IExampleRepository) -> None:
    await memory_impl.test_list(repo)


@pytest.mark.integration
async def test_delete_one(repo: IExampleRepository) -> None:
    await memory_impl.test_delete_one(repo)


@pytest.mark.integration
async def test_delete_one_no_id_error(repo: IExampleRepository) -> None:
    await memory_impl.test_delete_one_no_id_error(repo)


@pytest.mark.integration
async def test_delete_one_not_found_error(repo: IExampleRepository) -> None:
    await memory_impl.test_delete_one_not_found_error(repo)


@pytest.mark.integration
async def test_delete(repo: IExampleRepository) -> None:
    await memory_impl.test_delete(repo)
