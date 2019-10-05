"""Module that contains utility functions."""

from decimal import Decimal, ROUND_HALF_UP


def round_up(value, half_it=False):
    if half_it:
        value /= 2
    result = Decimal(value).to_integral_value(rounding=ROUND_HALF_UP)
    return int(result)
