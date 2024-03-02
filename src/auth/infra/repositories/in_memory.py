from auth.domain.entities import Client
from auth.domain.repository import IClientRepository
from auth.domain.uow import IAuthUnitOfWork
from shared.infra.in_memory.repository import InMemoryRepository
from shared.infra.in_memory.uow import InMemoryUnitOfWork
from shared.infra.in_memory.utils import id_int_gen, create_at_gen


class ClientInMemoryRepository(InMemoryRepository, IClientRepository):
    model = Client
    field_gens = {
        "id": id_int_gen,
        "date_joined": create_at_gen,
    }


class AuthInMemoryUnitOfWork(InMemoryUnitOfWork, IAuthUnitOfWork):
    pass
