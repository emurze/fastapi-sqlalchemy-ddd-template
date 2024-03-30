from auth.domain.entities import Account
from auth.infra.models import AccountModel
from seedwork.domain.mapper import IDataMapper


class AccountMapper(IDataMapper):
    entity_class = Account
    model_class = AccountModel

    def entity_to_model(self, entity: Account) -> AccountModel:
        dummy_kw = entity.model_dump()
        return self.model_class(**dummy_kw)

    def model_to_entity(self, model: AccountModel) -> Account:
        dummy_kw = model.as_dict()
        return self.entity_class(**dummy_kw)
