from pydantic_settings import BaseSettings


class CacheConfig(BaseSettings):
    cache_port: int
    cache_host: str
    cache_db: int

    def get_dsn(self, driver: str = 'redis') -> str:
        return '{}://{}:{}/{}'.format(
            driver,
            self.cache_host,
            self.cache_port,
            self.cache_db,
        )


def get_cache_dsn():
    cache_config = CacheConfig()
    return cache_config.get_dsn()
