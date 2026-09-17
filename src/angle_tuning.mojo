# Exact tuning of a rational ray address by a hyperbolic component.
#
# Douady's tuning substitutes the binary expansion of an angle by the two
# root-ray blocks of a component. Let the component have root rays
# `theta_- < theta_+`, both of period `n`, and let `theta` be a periodic angle
# of period `q`. Write the `q` binary digits of `theta`; replace each `0` by
# the `n` digits of `theta_-` and each `1` by the `n` digits of `theta_+`. The
# resulting `n q` digits are the period of the tuned angle, so the tuned angle
# is that word read as an integer over `2^(n q) - 1`.
#
# This module is the Mojo-side derivation of the tuned angles that
# `C1_residual_directive_carrier` checks its star product against. Those
# instances used to appear there only as literals, computed elsewhere: the
# substitution side was executed here and the angle side was not, so the
# agreement of the two was asserted rather than derived. `tuned_angle` closes
# that: the smoke now tunes the angle and compares.
#
# All arithmetic is checked fixed-width integer arithmetic. A digit of a
# reduced address `p/q` is read by doubling `p` and comparing with `q`, which
# cannot exceed `2q`, and the tuned denominator `2^(n q) - 1` is refused
# before it is formed unless `n q` stays inside `TUNING_PERIOD_LIMIT`. There
# is no floating point and no measured angle here; these are finite symbolic
# addresses.
#
# Scope: tuning is an operation on addresses. It locates no parameter in the
# plane, and the landing of the tuned ray is the imported theorem tag, not a
# property computed here.

from checked_int64_backend import CheckedI64Result, checked_add_i64, checked_mul_i64, checked_sub_i64
from checked_ray_address import (
    CheckedRayAddrResult,
    checked_double_ray_addr,
    checked_ray_addr_equal,
    make_checked_ray_addr,
    rejected_ray_addr,
)

# `2^62 - 1` is the largest tuned denominator that fits, so a period product
# beyond 62 is refused rather than wrapped.
comptime TUNING_PERIOD_LIMIT = 62


struct BinaryBlock(Copyable, Movable):
    """The leading binary digits of an address, or a rejection."""

    var digits: List[Int]
    var rejected: Bool

    def __init__(out self, digits: List[Int], rejected: Bool):
        self.digits = digits.copy()
        self.rejected = rejected

    def accepted(self) -> Bool:
        return not self.rejected

    def length(self) -> Int:
        return len(self.digits)


def rejected_block() -> BinaryBlock:
    return BinaryBlock(List[Int](), True)


def angle_period(num: Int64, den: Int64) -> Int:
    """Exact period of `num/den` under doubling modulo one, or `-1`.

    Refuses an address outside `(0, 1)`, an address whose reduced denominator
    is even (those are strictly preperiodic, not periodic), any overflow, and
    a period beyond `TUNING_PERIOD_LIMIT`."""
    var start = make_checked_ray_addr(num, den)
    if start.rejected or start.num == 0 or start.den % 2 == 0:
        return -1
    var current = checked_double_ray_addr(start)
    for period in range(1, TUNING_PERIOD_LIMIT + 1):
        if current.rejected:
            return -1
        if checked_ray_addr_equal(current, start):
            return period
        current = checked_double_ray_addr(current)
    return -1


def binary_block(num: Int64, den: Int64, length: Int) -> BinaryBlock:
    """The first `length` binary digits of `num/den`.

    Digit `k` is the integer part of `2^(k+1) num / den` modulo two, read by
    doubling the numerator and subtracting the denominator when it fits."""
    if length < 0:
        return rejected_block()
    var address = make_checked_ray_addr(num, den)
    if address.rejected:
        return rejected_block()
    var digits = List[Int]()
    var numerator = address.num
    for _ in range(length):
        var doubled = checked_mul_i64(numerator, 2)
        if doubled.overflowed:
            return rejected_block()
        if doubled.value >= address.den:
            var reduced = checked_sub_i64(doubled.value, address.den)
            if reduced.overflowed:
                return rejected_block()
            digits.append(1)
            numerator = reduced.value
        else:
            digits.append(0)
            numerator = doubled.value
    return BinaryBlock(digits^, False)


def _digits_to_numerator(digits: List[Int]) -> CheckedI64Result:
    """Read a binary word as an integer, most significant digit first."""
    var value = CheckedI64Result(0, False)
    for i in range(len(digits)):
        var shifted = checked_mul_i64(value.value, 2)
        if shifted.overflowed:
            return shifted^
        value = checked_add_i64(shifted.value, Int64(digits[i]))
        if value.overflowed:
            return value^
    return value^


def _period_denominator(period: Int) -> CheckedI64Result:
    """`2^period - 1`, the denominator of an address of that exact period."""
    if period < 1 or period > TUNING_PERIOD_LIMIT:
        return CheckedI64Result(0, True)
    var power = CheckedI64Result(1, False)
    for _ in range(period):
        power = checked_mul_i64(power.value, 2)
        if power.overflowed:
            return power^
    return checked_sub_i64(power.value, 1)


def tuned_angle(
    root_minus_num: Int64,
    root_minus_den: Int64,
    root_plus_num: Int64,
    root_plus_den: Int64,
    num: Int64,
    den: Int64,
) -> CheckedRayAddrResult:
    """`theta` tuned by the component with root rays `theta_- < theta_+`.

    Refuses a root pair whose two periods disagree, a non-periodic argument,
    a period product beyond `TUNING_PERIOD_LIMIT`, and any overflow. The
    result is a reduced address."""
    var root_period = angle_period(root_minus_num, root_minus_den)
    if root_period < 1 or angle_period(root_plus_num, root_plus_den) != root_period:
        return rejected_ray_addr()
    var angle_length = angle_period(num, den)
    if angle_length < 1:
        return rejected_ray_addr()
    if angle_length > TUNING_PERIOD_LIMIT // root_period:
        return rejected_ray_addr()

    var lower = binary_block(root_minus_num, root_minus_den, root_period)
    var upper = binary_block(root_plus_num, root_plus_den, root_period)
    var angle = binary_block(num, den, angle_length)
    if lower.rejected or upper.rejected or angle.rejected:
        return rejected_ray_addr()

    var word = List[Int]()
    for i in range(angle.length()):
        ref block = upper.digits if angle.digits[i] == 1 else lower.digits
        for j in range(len(block)):
            word.append(block[j])

    var numerator = _digits_to_numerator(word)
    var denominator = _period_denominator(root_period * angle_length)
    if numerator.overflowed or denominator.overflowed or denominator.value <= 0:
        return rejected_ray_addr()
    return make_checked_ray_addr(numerator.value, denominator.value)


def tunes_to(
    root_minus_num: Int64,
    root_minus_den: Int64,
    root_plus_num: Int64,
    root_plus_den: Int64,
    num: Int64,
    den: Int64,
    expected_num: Int64,
    expected_den: Int64,
) -> Bool:
    """Whether tuning `num/den` by the given component yields `expected`."""
    return checked_ray_addr_equal(
        tuned_angle(root_minus_num, root_minus_den, root_plus_num, root_plus_den, num, den),
        make_checked_ray_addr(expected_num, expected_den),
    )


# --- non-claims ---------------------------------------------------------------


def tuning_locates_a_parameter() -> Bool:
    # Tuning maps addresses to addresses. Associating a parameter with the
    # tuned address needs a landing theorem tag and an adapter, not this.
    return False


# --- smoke ------------------------------------------------------------------------


def angle_tuning_smoke() -> Bool:
    # Periods under doubling: 1/3 has period two, 1/7 three, 7/15 four, 2/5 four.
    if angle_period(1, 3) != 2 or angle_period(1, 7) != 3:
        return False
    if angle_period(7, 15) != 4 or angle_period(2, 5) != 4:
        return False
    # A strictly preperiodic address has no period, and neither has 0 or 1.
    if angle_period(1, 2) != -1 or angle_period(1, 6) != -1:
        return False
    if angle_period(0, 1) != -1 or angle_period(1, 1) != -1 or angle_period(1, 0) != -1:
        return False

    # The root blocks the substitution uses.
    var one_third: List[Int] = [0, 1]
    var two_thirds: List[Int] = [1, 0]
    var one_seventh: List[Int] = [0, 0, 1]
    var seven_fifteenths: List[Int] = [0, 1, 1, 1]
    if binary_block(1, 3, 2).digits != one_third:
        return False
    if binary_block(2, 3, 2).digits != two_thirds:
        return False
    if binary_block(1, 7, 3).digits != one_seventh:
        return False
    if binary_block(7, 15, 4).digits != seven_fifteenths:
        return False
    if binary_block(1, 0, 2).accepted() or binary_block(1, 3, -1).accepted():
        return False

    # The tuned instances the residual directive carrier checks its star
    # product against, derived here rather than quoted: the doubling component
    # (1/3, 2/3), the rabbit (1/7, 2/7), and the primitive period-four
    # component (7/15, 8/15).
    if not tunes_to(1, 3, 2, 3, 1, 3, 2, 5):
        return False
    if not tunes_to(1, 3, 2, 3, 2, 5, 7, 17):
        return False
    if not tunes_to(7, 15, 8, 15, 1, 3, 8, 17):
        return False
    if not tunes_to(1, 7, 2, 7, 1, 3, 10, 63):
        return False
    if not tunes_to(1, 7, 2, 7, 3, 7, 82, 511):
        return False

    # Tuning by the doubling component fixes nothing and is not the identity.
    if tunes_to(1, 3, 2, 3, 1, 3, 1, 3):
        return False
    # Fail closed: mismatched root periods, a non-periodic argument, and a
    # period product past the bound.
    if tuned_angle(1, 3, 1, 7, 1, 3).accepted():
        return False
    if tuned_angle(1, 3, 2, 3, 1, 6).accepted():
        return False
    if tuned_angle(1, 2047, 2, 2047, 1, 2047).accepted():
        return False
    return not tuning_locates_a_parameter()
