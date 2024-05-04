from seedwork.domain.rules import BusinessRule


class ExampleNameLengthMustBeGreaterThan5(BusinessRule):
    __message = "Example name length must be more than 5 characters"

    name: str

    def is_broken(self) -> bool:
        return len(self.name) <= 5
