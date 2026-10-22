"""Correctly rounded 50-digit roots using exact rational bounds."""

from decimal import MAX_EMAX, MIN_EMIN, ROUND_HALF_EVEN, Context, Decimal, localcontext
from fractions import Fraction
from math import isqrt


def sqrt_ratio_50(value: Fraction) -> Decimal:
    if type(value) is not Fraction or value < 0:
        raise ValueError("nonnegative exact ratio required")
    if not value:
        return Decimal("0")
    numerator, denominator = value.numerator, value.denominator
    a, b = isqrt(numerator), isqrt(denominator)
    context = Context(prec=50, rounding=ROUND_HALF_EVEN, Emax=MAX_EMAX, Emin=MIN_EMIN)
    with localcontext(context):
        if a * a == numerator and b * b == denominator:
            return Decimal(a) / Decimal(b)
    # Obtain the root's decimal exponent by integer comparisons, with no float.
    exponent = (len(str(numerator)) - len(str(denominator))) // 2

    def below(power: int) -> bool:
        return (
            numerator < denominator * 10 ** (2 * power)
            if power >= 0
            else numerator * 10 ** (-2 * power) < denominator
        )

    while below(exponent):
        exponent -= 1
    while not below(exponent + 1):
        exponent += 1
    for extra in range(8, 1001, 8):
        scale_power = 49 - exponent + extra
        scaled = (
            value * 10 ** (2 * scale_power)
            if scale_power >= 0
            else value / Fraction(10 ** (-2 * scale_power))
        )
        lower = isqrt(scaled.numerator // scaled.denominator)
        if scale_power >= 0:
            lo, hi = Fraction(lower, 10**scale_power), Fraction(lower + 1, 10**scale_power)
        else:
            lo, hi = (
                Fraction(lower * 10 ** (-scale_power)),
                Fraction((lower + 1) * 10 ** (-scale_power)),
            )
        with localcontext(context):
            rounded_lo = Decimal(lo.numerator) / Decimal(lo.denominator)
            rounded_hi = Decimal(hi.numerator) / Decimal(hi.denominator)
        if rounded_lo == rounded_hi:
            return rounded_lo
    raise ArithmeticError("unresolved exact root bounds")
