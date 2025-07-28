# app/schemas/calculation.py
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, condecimal, field_validator, FieldValidationInfo


class _CalcBase(BaseModel):
    a: condecimal(allow_inf_nan=False)  # supports int & Decimal
    b: condecimal(allow_inf_nan=False)
    type: Literal["add", "sub", "multiply", "divide"]

    # Pydantic v2 style validator
    @field_validator("b", mode="after")
    def no_zero_divisor(cls, v, info: FieldValidationInfo):
        """
        If the operation is 'divide', 'b' may not be zero.
        """
        if info.data.get("type") == "divide" and v == 0:
            raise ValueError("Division by zero")
        return v


class CalculationCreate(_CalcBase):
    """
    Incoming payload – no id / result yet.
    """
    pass


class CalculationRead(_CalcBase):
    """
    Outgoing payload – includes id and result.
    """
    id: int
    result: Decimal | None

    model_config = {"from_attributes": True}  # replaces orm_mode in v2
