import pytest

from tests.shared.conftest import IExampleUnitOfWork
from tests.shared.infra.memory import test_uow as uow_imp

example_dict = {"name": "example 1"}


@pytest.mark.integration
async def test_can_rollback(uow: IExampleUnitOfWork) -> None:
    await uow_imp.test_can_rollback(uow)


@pytest.mark.integration
async def test_can_commit(uow: IExampleUnitOfWork) -> None:
    await uow_imp.test_can_commit(uow)


@pytest.mark.integration
async def test_can_commit_rollback_rollback_commit_commit_rollback(
    uow: IExampleUnitOfWork,
) -> None:
    await uow_imp.test_can_commit_rollback_rollback_commit_commit_rollback(uow)
