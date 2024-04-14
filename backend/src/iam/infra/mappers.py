from iam.domain.entities import Account
from iam.infra.models import AccountModel
from seedwork.domain.mappers import IDataMapper


class AccountMapper(IDataMapper):
    def model_to_entity(self, model: AccountModel) -> Account:
        return Account(**model.as_dict())

    def entity_to_model(self, entity: Account) -> AccountModel:
        return AccountModel(**entity.model_dump())
