# tests/unit/test_calculation_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.calculation import CalculationCreate


@pytest.mark.parametrize(
    "payload",
    [
        {"a": 10, "b": 5, "type": "add"},
        {"a": 10, "b": 5, "type": "sub"},
        {"a": 10, "b": 5, "type": "multiply"},
        {"a": 10, "b": 5, "type": "divide"},
    ],
)
def test_create_valid(payload):
    obj = CalculationCreate(**payload)
    assert obj.a == payload["a"]  # parses OK


def test_divide_by_zero_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="divide")
