from dependency_injector import providers


def _link(obj):
    return providers.Singleton(lambda: obj)


def _group(*singletons):
    def inner(*args) -> list:
        return list(args)

    return providers.Singleton(inner, *singletons)


Link = _link
Group = _group
