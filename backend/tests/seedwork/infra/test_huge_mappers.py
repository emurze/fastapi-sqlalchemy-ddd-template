import pytest

from seedwork.domain.structs import alist
from tests.seedwork.confdata.domain import Example, ExampleItem, Address
from tests.seedwork.confdata.ports import ITestUnitOfWork


class PostGroup:
    pass


class Post:
    pass


class Tag:
    pass


class Comment:
    pass


class Complaint:
    pass


class PostGroupModel:
    pass


@pytest.mark.integration
async def test_mapper_can_update_5_tables(sql_uow: ITestUnitOfWork) -> None:
    pass


@pytest.mark.unit
async def test_mem_mapper_updates_5_tables(mem_uow: ITestUnitOfWork) -> None:
    await test_mapper_can_update_5_tables(mem_uow)