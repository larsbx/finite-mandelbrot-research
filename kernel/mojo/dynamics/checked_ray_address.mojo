# Rejection-aware Int64 rational ray-address primitives.
# Specification: docs/rational-interval-arithmetic-spec.md (binding 6.2).
#
# These are finite modular addresses, not measured angles. Fixed-width overflow
# rejects the transition; accepted results are canonical reduced fractions.
# The c=-2 orbit certificate that lived here is retired: its certificate of
# record is the BigZ replay in `dynamics/bigq_ray_address.mojo`. What remains
# serves the kneading and tuning kernels that still import it.

from arithmetic.checked_int64_backend import checked_mul_i64
from finite_exact.integer_gcd import gcd_i64


struct CheckedRayAddrResult(ImplicitlyCopyable):
    var num: Int64
    var den: Int64
    var rejected: Bool

    def __init__(out self, num: Int64, den: Int64, rejected: Bool):
        self.num = num
        self.den = den
        self.rejected = rejected

    def accepted(self) -> Bool:
        return not self.rejected


def rejected_ray_addr() -> CheckedRayAddrResult:
    return CheckedRayAddrResult(0, 1, True)


def make_checked_ray_addr(num: Int64, den: Int64) -> CheckedRayAddrResult:
    if den <= 0 or num < 0 or num >= den:
        return rejected_ray_addr()
    var divisor: Int64
    try:
        divisor = gcd_i64(num, den)
    except:
        return rejected_ray_addr()
    if divisor == 0:
        return rejected_ray_addr()
    return CheckedRayAddrResult(num // divisor, den // divisor, False)


def checked_ray_addr_equal(a: CheckedRayAddrResult, b: CheckedRayAddrResult) -> Bool:
    return not a.rejected and not b.rejected and a.num == b.num and a.den == b.den


def checked_double_ray_addr(address: CheckedRayAddrResult) -> CheckedRayAddrResult:
    if address.rejected:
        return rejected_ray_addr()
    var doubled = checked_mul_i64(address.num, 2)
    if doubled.overflowed:
        return rejected_ray_addr()
    return make_checked_ray_addr(doubled.value % address.den, address.den)


def checked_ray_address_smoke() -> Bool:
    var third = checked_double_ray_addr(make_checked_ray_addr(1, 3))
    var malformed = make_checked_ray_addr(1, 0)
    var overflowing = checked_double_ray_addr(make_checked_ray_addr(5000000000000000000, 9000000000000000001))
    return (
        checked_ray_addr_equal(third, make_checked_ray_addr(2, 3)) and
        malformed.rejected and overflowing.rejected
    )
