from seedwork.application.dtos import DTO


class EventResult(DTO):
    def is_success(self):
        return not self.error
