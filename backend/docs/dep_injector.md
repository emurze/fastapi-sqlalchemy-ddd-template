# Dependency Injector

### Factory

```
class Photo:
    def __str__(self) -> str:
        return "<Photo>"


@dataclass(frozen=True, slots=True)
class User:
    id: int
    photo: Photo


class Container(containers.DeclarativeContainer):
    user_factory = providers.Factory(User, photo=Photo)


if __name__ == '__main__':
    container = Container()
    user = container.user_factory(1)
    print(user)
```