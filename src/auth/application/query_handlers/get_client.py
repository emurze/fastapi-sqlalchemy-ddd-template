from dataclasses import dataclass

from auth.application.queries.get_client import (
    GetClientQuery,
    GetClientResult,
    GetClientPayload,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.query_handler import IQueryHandler
from shared.domain.exceptions import ResourceNotFoundError


@dataclass(frozen=True, slots=True)
class GetClientHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientQuery) -> GetClientResult:
        try:
            query_dict = query.model_dump()
            async with self.uow:
                client = await self.uow.clients.get(**query_dict)
                payload = GetClientPayload.model_validate(client)
                return GetClientResult(payload=payload)
        except ResourceNotFoundError:
            return GetClientResult.build_resource_not_found_error()
        except SystemError:
            return GetClientResult.build_system_error()
