from tests.utils.config import TestCacheConfig


def get_cache_dsn() -> str:
    cache_config = TestCacheConfig()
    return cache_config.get_dsn()
