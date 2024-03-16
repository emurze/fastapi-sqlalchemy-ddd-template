# import pytest
#
# from shared.domain.repositories import IGenericRepository
# from tests.shared.infra.memory import test_repository as memory_impl
#
#
# @pytest.mark.integration
# async def test_can_create_and_get(repo: IGenericRepository) -> None:
#     await memory_impl.test_can_create_and_get(repo)
#
#
# @pytest.mark.integration
# async def test_get_not_found_error(repo: IGenericRepository) -> None:
#     await memory_impl.test_get_not_found_error(repo)
#
#
# @pytest.mark.integration
# async def test_can_get_for_update(repo: IGenericRepository) -> None:
#     await memory_impl.test_can_get_for_update(repo)
#
#
# @pytest.mark.integration
# async def test_get_for_update_not_found_error(
#     repo: IGenericRepository,
# ) -> None:
#     await memory_impl.test_get_for_update_not_found_error(repo)
#
#
# @pytest.mark.integration
# async def test_list(repo: IGenericRepository) -> None:
#     await memory_impl.test_list(repo)
#
#
# @pytest.mark.integration
# async def test_delete_all(repo: IGenericRepository) -> None:
#     await memory_impl.test_delete_all(repo)
#
#
# @pytest.mark.integration
# async def test_delete_one(repo: IGenericRepository) -> None:
#     await memory_impl.test_delete_one(repo)
