# Alembic

```
alembic init <dir_name>

# alembic init src/migrations

alembic revision --autogenerate -m <revision>

alembic upgrade head  # upgrade to the last migration

alembic upgrade head <revision>  # upgrade to the definite migration 
```

### alembic.ini

```bash
prepend_sys_path = . src  # imports src to migrations
```

### You can reset alembic.ini vars in migrations/env.py

```python
config.set_main_option(
    "sqlalchemy.url",
    c.db.get_dsn() + "?async_fallback=True"
)

target_metadata = ...
```