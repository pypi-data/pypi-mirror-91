from __future__ import annotations

from enum import Enum
from functools import total_ordering
from typing import Optional, Union

__all__ = (
    "Infinity",
    "Number",
    "Sign",
    "INFINITY",
    "NEGATIVE_INFINITY",
    "POSITIVE_INFINITY",
)


class Sign(Enum):
    Negative = -1
    Positive = 1

    def __neg__(self) -> Sign:
        return __class__.Negative if self else __class__.Positive

    def __bool__(self) -> bool:
        return self == __class__.Positive

    def __mul__(self, rhs) -> Sign:
        return __class__(self.value * rhs.value)

    def __str__(self) -> str:
        return "" if self else "-"

    @classmethod
    def from_number(cls, v) -> Optional[Sign]:
        if v < 0:
            return cls.Negative
        if v > 0:
            return cls.Positive
        if v == 0:
            return None
        return NotImplemented


@total_ordering
class Infinity:
    sign: Sign

    __slots__ = ("sign",)

    def __init__(self, sign: Sign = Sign.Positive):
        self.sign = sign

    def __hash__(self):
        return hash((self.sign,))

    def __bool__(self) -> bool:
        return True

    def __pos__(self) -> Infinity:
        return self

    def __neg__(self) -> Infinity:
        return __class__(-self.sign)

    def __add__(self, rhs: Number) -> Number:
        if isinstance(rhs, Infinity) and self.sign != rhs.sign:
            return 0
        else:
            return self

    def __sub__(self, rhs: Number) -> Number:
        return self + -rhs

    def __floordiv__(self, rhs: Number) -> Number:
        if rhs == 0:
            raise ZeroDivisionError("division by zero")
        if isinstance(rhs, Infinity):
            return NotImplemented  # TODO
        return __class__(self.sign * Sign.from_number(rhs))

    def __mod__(self, rhs: Number) -> Number:
        if rhs == 0:
            raise ZeroDivisionError("modulo by zero")
        return NotImplemented  # TODO

    def __mul__(self, rhs: Number) -> Number:
        if rhs == 0:
            return 0
        if isinstance(rhs, Infinity):
            return __class__(self.sign * rhs.sign)
        return __class__(self.sign * Sign.from_number(rhs))

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, lhs: Number) -> Number:
        return -self + lhs

    def __rfloordiv__(self, lhs: Number) -> Number:
        if isinstance(lhs, Infinity):
            return NotImplemented  # TODO
        return 0

    def __rmod__(self, lhs: Number) -> Number:
        return NotImplemented  # TODO

    def __le__(self, rhs: Number) -> bool:
        return self.sign == Sign.Negative or self == rhs

    def __eq__(self, rhs: object) -> bool:
        return isinstance(rhs, Infinity) and rhs.sign == self.sign

    def __str__(self) -> str:
        return f"{self.sign}\N{INFINITY}"

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.sign.name})"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> Infinity:
        """Validates and parses `v` to infinity"""
        if not isinstance(v, str):
            raise TypeError(f"must be str, not {type(v)}")
        v = v.lower().replace("\N{INFINITY}", "infinity")
        if v == "infinity":
            return INFINITY
        if v == "-infinity":
            return -INFINITY
        raise ValueError(
            f"expected infinity or -infinity in any case, not {v}"
        )

    def serialize(self) -> str:
        return f"{self.sign}infinity"


Number = Union[int, Infinity]

INFINITY = Infinity()
POSITIVE_INFINITY = +INFINITY
NEGATIVE_INFINITY = -INFINITY
