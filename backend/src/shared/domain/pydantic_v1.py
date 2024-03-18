from pydantic.v1 import Field as V1Field, ValidationError as V1ValidationError
from pydantic.v1.dataclasses import dataclass as v1_dataclass

Field = V1Field
ValidationError = V1ValidationError
py_dataclass = v1_dataclass
