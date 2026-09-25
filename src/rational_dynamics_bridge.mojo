# Differential bridge to the shared rational_dynamics R1 kernel.
# Specification: docs/rational-interval-arithmetic-spec.md (binding 6.2).
#
# This file does not replace the consumer's existing BigQRayAddr path. It
# checks that the shared finite-arithmetic kernel agrees on the overlapping
# symbolic-fraction operations before any authority migration is considered.

from finite_exact.bigint_z import bigz_eq, bigz_from_i64
from bigq_ray_address import make_bigq_ray_addr, bigq_double_ray_addr
from rational_dynamics.rational import (
    continued_fraction,
    convergents,
    double_mod_one,
    farey_determinant,
    fraction_from_i64,
    mod_inverse,
    signed_mod_inverse,
)


def _same_fraction(shared, local) -> Bool:
    return (
        shared.accepted() and local.accepted() and
        bigz_eq(shared.num, local.value.num) and
        bigz_eq(shared.den, local.value.den)
    )


def rational_dynamics_r1_bridge_smoke() -> Bool:
    # The existing BigQ symbolic-address implementation and shared R1 agree
    # on doubling modulo one.
    var shared_one_third = fraction_from_i64(1, 3)
    var local_one_third = make_bigq_ray_addr(bigz_from_i64(1), bigz_from_i64(3))
    var shared_doubled = double_mod_one(shared_one_third)
    var local_doubled = bigq_double_ray_addr(local_one_third)
    if not _same_fraction(shared_doubled, local_doubled):
        return False

    # Arithmetic that previously lived only in the Ford-side research code is
    # now available from the neutral kernel.
    var two_fifths = fraction_from_i64(2, 5)
    var inverse = mod_inverse(two_fifths)
    var centered = signed_mod_inverse(two_fifths)
    if inverse.rejected or centered.rejected:
        return False
    if not bigz_eq(inverse.num, bigz_from_i64(3)):
        return False
    if not bigz_eq(centered.num, bigz_from_i64(-2)):
        return False

    var three_sevenths = fraction_from_i64(3, 7)
    var expansion = continued_fraction(three_sevenths)
    var conv = convergents(three_sevenths)
    if expansion.rejected or conv.rejected:
        return False
    if len(expansion.terms) != 3 or len(conv.denominators) != 3:
        return False
    if not (
        bigz_eq(expansion.terms[0], bigz_from_i64(0)) and
        bigz_eq(expansion.terms[1], bigz_from_i64(2)) and
        bigz_eq(expansion.terms[2], bigz_from_i64(3)) and
        bigz_eq(conv.denominators[1], bigz_from_i64(2)) and
        bigz_eq(conv.denominators[2], bigz_from_i64(7))
    ):
        return False

    var determinant = farey_determinant(
        fraction_from_i64(1, 3),
        fraction_from_i64(2, 5),
    )
    return (
        determinant.accepted() and
        bigz_eq(determinant.value, bigz_from_i64(-1)) and
        fraction_from_i64(-1, 3).rejected
    )
