from decimal import Decimal
from enum import Enum

from sqlalchemy import Column, Integer, Numeric, Enum as PgEnum
from app.database import Base


class CalcType(str, Enum):
    add = "add"
    sub = "sub"
    multiply = "multiply"
    divide = "divide"


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Numeric(scale=4), nullable=False)
    b = Column(Numeric(scale=4), nullable=False)
    type = Column(PgEnum(CalcType, name="calctype"), nullable=False)
    result = Column(Numeric(scale=4), nullable=True)

    def compute(self) -> Decimal:
        """Return the arithmetic result without persisting."""
        if self.type == CalcType.add:
            return self.a + self.b
        if self.type == CalcType.sub:
            return self.a - self.b
        if self.type == CalcType.multiply:
            return self.a * self.b
        if self.type == CalcType.divide:
            if self.b == 0:
                raise ZeroDivisionError("Division by zero")
            return self.a / self.b
        raise ValueError(f"Unsupported op {self.type}")
