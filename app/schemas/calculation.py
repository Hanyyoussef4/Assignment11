# app/schemas/calculation.py
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, condecimal, model_validator


class _CalcBase(BaseModel):
    a: condecimal(allow_inf_nan=False)
    b: condecimal(allow_inf_nan=False)
    type: Literal["add", "sub", "multiply", "divide"]

    @model_validator(mode="after")
    def no_zero_divisor(cls, values):
        """
        After all fields are parsed, forbid dividing by zero.
        """
        if values.type == "divide" and values.b == 0:
            raise ValueError("Division by zero")
        return values


class CalculationCreate(_CalcBase):
    """Incoming payload – no id/result yet."""
    pass


class CalculationRead(_CalcBase):
    """Outgoing payload – includes id and result."""
    id: int
    result: Decimal | None

    model_config = {"from_attributes": True}  # replaces orm_mode in Pydantic v2
