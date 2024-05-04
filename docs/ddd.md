# Domain Features

* ```__hash__ and __eq__``` for using in set and dict keys

```python
# Entity

class Batch(Model):
    reference: int = Field(frozen=True)
    CKU: str
    purchased_quantity: int
    ETA: Optional[datetime.datetime] = None
    allocated_lines: set[OrderLine] = Field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.reference)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference


# Value Object

class OrderLine(BaseModel, frozen=True):
    order_ref: int
    CKU: str
    quantity: int

    def __hash__(self) -> int:
        return hash((self.order_ref, self.CKU, self.quantity))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderLine):
            return False
        return all([
            self.order_ref == other.order_ref,
            self.CKU == other.CKU,
            self.quantity == other.quantity
        ])
```

* ```__gt__``` for using in sorted() without key

# Domain Model and Repository

### Mapper

```python
def start_mapper() -> None:
    mapped_registry.map_imperatively(Post, table)
```

### Repository

* is memory, think so
  * no .save()
  * .commit() is delegated to a call side

* methods
  * .add()
  * .get()
  * .list()

* delete to obj.cancel()

* update to a Unit Of Work pattern

```python
@dataclass(frozen=True, slots=True)
class PostRepository(IPostRepository):
    session: AsyncSession

    def add(self, obj: Post) -> None:
        self.session.add(obj)

    async def get(self, **kw) -> Post:
        query = (
            select(Post)
            .filter_by(**kw)
        )
        res = await self.session.execute(query)
        return res.scalars().one()

    async def list(self) -> tuple[Post, ...]:
        res = await self.session.execute(select(Post))
        return tuple(res.scalars().all())


class FakePostRepository(IPostRepository):
    def __init__(self, posts: Iterable[Post]) -> None:
        self._posts = set(posts)

    def add(self, obj: Post) -> None:
        self._posts.add(obj)

    async def get(self, **kw) -> Post:
        return next(post for post in self._posts if post.validate_dict(**kw))

    async def list(self) -> tuple[Post, ...]:
        return tuple(self._posts)
```

### Pros

1. We focus to a business logic
    * Test -> business logic -> infra test -> infra changes + migration
    * Is not django where - infra test -> infra changes + migration -> test -> business logic  

2. Easy testing

3. No dependencies on infrastructure

### Cons

1. More difficult infra code, sometimes it requires you to change domain model

2. Extra code for repository

### Notes

1. Reusable repository requires only 1 set of tests
   * future tests for it will be small

2. Not always you need all of it like when you have a simple CRUD.

### Error Handling Flow

1. Presentation validation
2. Validated data maps to consistent(pydantic) command
3. Application returns result with errors from domain, infrastructure
4. Presentation raises result errors

### Slang

1. Architecture style is a pattern that is followed by a entire application.
2. Architecture pattern is a pattern that is followed by a part of code.