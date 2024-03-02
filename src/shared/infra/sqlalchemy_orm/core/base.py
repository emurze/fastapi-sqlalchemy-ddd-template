from typing import Any as MetaData
from collections.abc import Iterable

from shared.infra.sqlalchemy_orm.core import import_contracts, config
from shared.infra.sqlalchemy_orm.core.contract import DBContract
from shared.infra.sqlalchemy_orm import common


class Base:
    metadata: MetaData

    def __init__(self, contracts: Iterable[DBContract]) -> None:
        self.metadata = common.combine_metadata(c.metadata for c in contracts)
        self.mappers = [c.mapper_runner for c in contracts]

    def run_mappers(self) -> None:
        for mapper in self.mappers:
            mapper()


def get_base() -> Base:
    contracts = import_contracts.import_contracts(
        directory=config.PATH,
        filename=config.FILENAME,
        contract_varname=config.CONTRACT_VARNAME,
    )
    return Base(contracts)
