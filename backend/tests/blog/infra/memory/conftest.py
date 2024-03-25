import pytest

from blog.domain.repositories import IPostUnitOfWork, IPostRepository


@pytest.fixture(scope="function")
def uow(memory_container) -> IPostUnitOfWork:
    return memory_container.post_uow()


@pytest.fixture(scope="function")
def post_repo(memory_container) -> IPostRepository:
    return memory_container.post_repo()
