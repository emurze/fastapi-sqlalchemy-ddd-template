from spiking.domain.uows import IUnitOfWork
from spiking.domain.events import PostCreatedEvent, PostPublishedEvent


async def print_hello(event: PostCreatedEvent) -> None:
    print("Hello")


async def publish_post(event: PostCreatedEvent, uow: IUnitOfWork) -> None:
    post = await uow.posts.get_by_id(event.id, for_update=True)
    post.publish()
    print("Post published")
