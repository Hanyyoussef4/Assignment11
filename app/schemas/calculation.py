# app/schemas/calculation.py
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, condecimal, validator


class _CalcBase(BaseModel):
    a: condecimal(allow_inf_nan=False)  # support ints & decimals
    b: condecimal(allow_inf_nan=False)
    type: Literal["add", "sub", "multiply", "divide"]

    @validator("b")
    def no_zero_divisor(cls, v, values):
        """
        If the operation is 'divide', b may not be zero.
        """
        if values.get("type") == "divide" and v == 0:
            raise ValueError("Division by zero")
        return v


class CalculationCreate(_CalcBase):
    """
    Schema for *incoming* payloads (no id/result yet).
    """
    pass


class CalculationRead(_CalcBase):
    """
    Schema for *outgoing* payloads (includes id & result).
    """
    id: int
    result: Decimal | None

    class Config:
        orm_mode = True
