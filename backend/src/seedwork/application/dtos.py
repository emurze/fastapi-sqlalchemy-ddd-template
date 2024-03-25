from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    # todo: disable validation for performance
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
