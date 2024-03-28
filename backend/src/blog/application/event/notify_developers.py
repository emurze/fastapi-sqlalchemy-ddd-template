from blog.domain.events import PostAlreadyExist


async def notify_developers(event: PostAlreadyExist) -> None:
    print(f'NOTIFY {event}')
