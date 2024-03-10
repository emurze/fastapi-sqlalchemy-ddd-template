import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from post.domain.repositories import IPostUnitOfWork, IPostRepository


@pytest.fixture(scope="function")
def uow(container) -> IPostUnitOfWork:
    return container.post_uow()


@pytest.fixture(scope="function")
def post_repo(container, session: AsyncSession) -> IPostRepository:
    return container.post_repo(session)
