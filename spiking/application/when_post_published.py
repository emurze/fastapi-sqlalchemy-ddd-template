from spiking.domain.uows import IUnitOfWork
from spiking.domain.events import PostPublishedEvent


async def populate_post(event: PostPublishedEvent, uow: IUnitOfWork) -> None:
    post = await uow.posts.get_by_id(event.id)
    post.populate()
    print("Post populated")
