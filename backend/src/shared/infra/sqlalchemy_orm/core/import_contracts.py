import os
import importlib.util

from pathlib import Path

from shared.infra.sqlalchemy_orm.core.contract import DBContract


def import_contracts(
    directory: Path,
    filename: str,
    contract_varname: str,
) -> list[DBContract]:
    _contracts = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                module_name = os.path.splitext(file)[0]

                spec = importlib.util.spec_from_file_location(
                    module_name, Path(root, file)
                )

                if spec is None or spec.loader is None:
                    continue

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                contract = getattr(module, contract_varname)

                if contract is None:
                    continue

                _contracts.append(contract)

    return _contracts
