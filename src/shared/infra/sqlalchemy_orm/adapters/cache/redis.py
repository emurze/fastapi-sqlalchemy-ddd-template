from shared.infra.sqlalchemy_orm.ports import ICacheClient


class RedisCache(ICacheClient):
    def __init__(self, conn):
        pass
