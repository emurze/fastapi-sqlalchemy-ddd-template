# SqlAlchemy

### SqlAlchemy Core

* Engine 
  * Connection Pool
    ```
    pool.acquire() as conn
  
    # ...low_api_code...
  
    await conn.execute("...")
  
    pool.release(conn)
    ```
  * Dialect
    ```
    1. query.compile(dialect=dialect)  # different results
    
    2. Class PGDialect:
           """Depends on postrges features"""
      
       Class AsyncPGDriver(PGDialect):
           """Depends on driver features and PGDialect"""
    
    3. CustomDialect features using inspect()
       # get_indexes()
    ```
  * Engine -> Connection
  * Connection.execute() -> Row(labeled tuple), not Model,  
  
* SQL Expression Language
    ```
    # DDL
    
    ### Imperative syntax 
  
    Table(
        "table_name",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(256), nullable=True),
    )
    
    async with self.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # DML
  
    ### Injection
    
    
    *****************
  
    insert()
    .values()
    .where() | .filter()
    .filter_by()
  
    update()
    .values()
    .where()
  
    delete()
    .filter_by()
  
    # DQL
  
    select("*", "can't set this field")
  
    r = aliased(Model)
  
    sub_query = (
        select(
            w.id,
            w.name,
            r.compensation,
            cast(
                func.AVG(r.compensation).over(partition_by=r.workload),
                Integer,
            )
            .label("avg_workload_compensation")
        )
        .select_from(r)
        .join(w, r.worker_id == w.id)
        .subquery("helper1")
    )
    cte = (
        select(
            sub_query.c.id,
            sub_query.c.name,
            sub_query.c.compensation,
            (sub_query.c.compensation - sub_query.c.avg_workload_compensation)
             .label('compensation_diff'),
        )
        .cte("helper2")
    )
    query = (
        select(cte)
        .order_by(cte.c.compensation_diff.desc())
    )
    ```
  
* Schema / Types


### SqlAlchemy Orm

* Declarative Tables
  ```python
  async_engine = create_async_engine(
      config.db.get_dsn(),
      echo=True,
  )
  async_session_maker = async_sessionmaker(
      async_engine,
      autobegin=True,
  )
  
  str256 = Annotated[int, 256]
  
  
  class Base(DeclarativeBase):
      type_annotation_map = {
          str256: String(256),
      }
  
  
  async def get_session() -> Iterator[AsyncSession]:
      async with async_session_maker() as session:
          yield session
  ```

* Models
  ```python
  intpk = Annotated[int, mapped_column(primary_key=True)]
  created_at = Annotated[
      datetime.datetime, mapped_column(
          server_default=text("TIMEZONE('utc', now())"),
      )
  ]
  updated_at = Annotated[
      datetime.datetime, mapped_column(
          server_default=text("TIMEZONE('utc', now())"),
          default=datetime.datetime.utcnow,
      )
  ]
  
  
  class WorkerModel(Base):
      __tablename__ = 'worker'
  
      id: Mapped[intpk]
      name: Mapped[str256]
  
      resumes: Mapped[list["ResumeModel"]] = relationship()
  
  
  class ResumeModel(Base):
      __tablename__ = 'resume'
  
      id: Mapped[intpk]
      title: Mapped[str]
      compensation: Mapped[int | None]
      workload: Mapped[Literal["parttime", 'fulltime']]
      worker_id: Mapped[int] = mapped_column(
          ForeignKey("worker.id", ondelete="CASCADE")
      )
      created_at: Mapped[created_at]
      updated_at: Mapped[updated_at]

      worker: Mapped["WorkerModel"] = relationship()
  ```
  
* Query syntax
  ```
  # DML (Insert, Update, Delete)
  
  ### Core Features difference is returned Models
  
  stmt = (
      update(Model)
      .values(name=id)
      .filter_by(name=10)
  )
  await session.execute(stmt)
  
  stmt = (
      delete(Model)
      .filter_by(name=10)
  )
  await session.execute(stmt)
  
  ### Insert

  model = Model(**kwargs)
  model2 = Model(**kwargs)
  model3 = Model(**kwargs)
  
  session.add(model)
  session.add_all([model2, model3])
  await session.commit()
  
  .flush() - run triggers, signals on fields like id
  .refresh() - from db
  .expire_all() - remove all sessions, clear all done queries
  
  # DQL
  
  ### Single Object (Select, Update)
  
  await session.get(Model, 1)
  obj = await session.get(Model, {"id": 1})
  obj.name = "Vlad"  # second query
  await session.commit()
  
  ### Many Objects (Select)
  
  query = (
      select()
      .options(
          selectinload(Model.resumes)
          # or
          jsonedload(Model.resumes)
      )
  )  # Two queries to solve n+1 problem
  
  res = await session.execute(query)
  
  res.all()[0].resumes -> list[Model]
  ```

### How to define object relational mapping

* MetaData -> Table

* registry -> Mapped Classes


#### Declarative Mapping

1. Declarative Mapping using Base

```python
class Post(Base):
    __tablename__ = "post"

    id: Mapped[co.intpk]
    title: Mapped[str]
    created_at: Mapped[co.created_at]
    updated_at: Mapped[co.updated_at]  # todo: requires trigger
    draft: Mapped[bool] = True
```

2. Declarative Mapping using @mapped_registry.mapped

```python
mapped_registry = registry()


@mapped_registry.mapped
class Post:
    __tablename__ = "post"

    id: Mapped[co.intpk]
    title: Mapped[str]
    created_at: Mapped[co.created_at]
    updated_at: Mapped[co.updated_at]  # todo: requires trigger
    draft: Mapped[bool] = True
```

3. Declarative Mapping using Mapped and mapped_column

```python
class Post(Base):
    __tablename__ = "post"

    id: Mapped[co.intpk]
    title: Mapped[str]
    created_at: Mapped[co.created_at]
    updated_at: Mapped[co.updated_at]  # todo: requires trigger
    draft: Mapped[bool] = True
```

4. Declarative Mapping using Imperative Table
```python
class Post2(Base):
    __table__ = Table(
        "post2",
        post2_metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String),
        Column("created_at", DateTime,
               server_default=text("TIMEZONE('utc', now())")),
        Column("updated_at", DateTime,
               server_default=text("TIMEZONE('utc', now())"),
               onupdate=timezone.utc),
        Column("draft", Boolean, default=True),
    )
```

#### Imperative Mapping

```python
mapped_registry = registry()

post2 = Table(
    "post2",
    mapped_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("created_at", DateTime,
           server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", DateTime,
           server_default=text("TIMEZONE('utc', now())"),
           onupdate=timezone.utc),
    Column("draft", Boolean, default=True),
)


@dataclass
class Post2:
    id: int
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    draft: bool = True


mapped_registry.map_imperatively(Post2, post2)
```


### Attached to a different loop problem

Default Queue class .acquire(), .release() for many reused connections

* engine (connection pool) is queue with shared connections 

* task1 (own loop) -> takes a conn, execute this conn

* test2 (own loop) -> takes the conn, execute this conn

  ```error (Future pending) attached to a different loop```


#### Solution is to use NullPool

NullPool class returns always a new connection

* create_async_engine(dsn, poolclass=NullPool)

* task1 (own loop) -> takes a new conn, execute this conn

* task2 (own loop) -> takes a new conn, execute this conn

### Use sorted_tables, they are sorted by FK constraint

### RelationShip

1. Create 2 attributes for each domain

2. Set relationship in property

```python
# 1

class Post:
    publisher: ClassVar[Any]


class Publisher:
    posts: ClassVar[list[Post]]


# 2
    
def start_mapper() -> None:
    post_mapper = mapper_registry.map_imperatively(Post, post_table)
    mapper_registry.map_imperatively(
        Publisher,
        publisher_table,
        properties={
            "posts": relationship(
                post_mapper,
                backref="publisher",
            )
        },
    )
```

### ORM optimization tools

1. joinedload for OneToOne and ManyToOne

2. selectinload for OneToMany and ManyToMany

3. Crutch .unique() is python specific solution for bad used joinedload

```python
class PublisherRepository(
    SQLAlchemyRepositoryMixin[Publisher],
    IPublisherRepository,
):
    model = Publisher

    async def get_with_posts(self, **kw) -> Publisher:
        publisher_posts = cast(Any, Publisher.posts)
        query = (
            select(Publisher)
            .options(selectinload(publisher_posts))
            .filter_by(**kw)
        )
        res = await self.session.execute(query)
        return res.scalars().one()
```

1. Try .append() for relationship, or use set with .add() ???

2. __table_args__ for Indexes, Constraints ???

3. relationship(secondary=TableName), ManyToMany ???

4. contains_eager ???


### NullPool constraints you to make your tests small.

- Because db has max_connections property that is limited

- You can write only one concurrent test for your uow


### Transactions rewrites session instance

- It's allowed only in sequence of transaction, not in concurrent(async) flow

- But Async flow requires creating one new uow per handler, so that a uow is always async-safe

### Pool should have pool_size=10, max_overflow=0,