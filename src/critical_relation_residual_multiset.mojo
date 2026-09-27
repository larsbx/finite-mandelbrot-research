# critical_relation_residual_multiset.mojo
#
# Exact lower-type stripping for
#
#     A_{4,1}(C) = C^5(C+2)(C^3+2C^2+2C+2)F_7(C).
#
# The known roots C=0 and C=-2 already collide before type (4,1), and the
# cubic is a factor of A_{3,1}=C^4(C+2)(C^3+2C^2+2C+2), so each of its three
# roots collides at (3,1).  Their total multiplicity nine is removed.  The
# remaining degree-7 factor F_7 is an algebraic candidate divisor only: this
# module does not certify the exact type, embeddings, or localization of its
# roots.

from poly_z import (
    PolyZ,
    equal_poly,
    expected_F7_M41,
    expected_R_4_1_factorized,
    raw_return_poly,
)
from critical_relation_bridge import synthetic_divide_monic_linear
from critical_relation_multiset import integer_exact_minimal_collision_pattern


struct LinearPowerStripResult:
    var quotient: PolyZ
    var divisions: Int
    var exact: Bool

    def __init__(
        out self, quotient: PolyZ, divisions: Int, exact: Bool
    ):
        self.quotient = quotient.copy()
        self.divisions = divisions
        self.exact = exact


struct PolyDivisionResult:
    var quotient: PolyZ
    var exact: Bool

    def __init__(out self, quotient: PolyZ, exact: Bool):
        self.quotient = quotient.copy()
        self.exact = exact


struct R41ResidualDivisorMultiset(ImplicitlyCopyable):
    var relation_degree: Int
    var zero_multiplicity: Int
    var minus_two_multiplicity: Int
    var cubic_multiplicity: Int
    var stripped_lower_type_multiplicity: Int
    var residual_degree: Int
    var degree_accounting_exact: Bool
    var relation_factorization_exact: Bool
    var residual_factorization_exact: Bool
    var known_roots_rejected_by_exact_type: Bool
    var cubic_collides_at_3_1: Bool
    var residual_exact_type_certified: Bool
    var rejected: Bool

    def __init__(
        out self,
        relation_degree: Int,
        zero_multiplicity: Int,
        minus_two_multiplicity: Int,
        cubic_multiplicity: Int,
        stripped_lower_type_multiplicity: Int,
        residual_degree: Int,
        degree_accounting_exact: Bool,
        relation_factorization_exact: Bool,
        residual_factorization_exact: Bool,
        known_roots_rejected_by_exact_type: Bool,
        cubic_collides_at_3_1: Bool,
        residual_exact_type_certified: Bool,
        rejected: Bool,
    ):
        self.relation_degree = relation_degree
        self.zero_multiplicity = zero_multiplicity
        self.minus_two_multiplicity = minus_two_multiplicity
        self.cubic_multiplicity = cubic_multiplicity
        self.stripped_lower_type_multiplicity = stripped_lower_type_multiplicity
        self.residual_degree = residual_degree
        self.degree_accounting_exact = degree_accounting_exact
        self.relation_factorization_exact = relation_factorization_exact
        self.residual_factorization_exact = residual_factorization_exact
        self.known_roots_rejected_by_exact_type = known_roots_rejected_by_exact_type
        self.cubic_collides_at_3_1 = cubic_collides_at_3_1
        self.residual_exact_type_certified = residual_exact_type_certified
        self.rejected = rejected

    def algebraic_replay_accepted(self) -> Bool:
        return (
            not self.rejected and self.relation_degree == 16 and
            self.zero_multiplicity == 5 and
            self.minus_two_multiplicity == 1 and
            self.cubic_multiplicity == 1 and
            self.stripped_lower_type_multiplicity == 9 and
            self.residual_degree == 7 and
            self.degree_accounting_exact and
            self.relation_factorization_exact and
            self.residual_factorization_exact and
            self.known_roots_rejected_by_exact_type and
            self.cubic_collides_at_3_1
        )

    def exact_type_divisor_accepted(self) -> Bool:
        return (
            self.algebraic_replay_accepted() and
            self.residual_exact_type_certified
        )

    def proves_density(self) -> Bool:
        return False

    def proves_equidistribution(self) -> Bool:
        return False

    def proves_c1(self) -> Bool:
        return False


def strip_monic_linear_power(
    poly: PolyZ, root: Int, requested_power: Int
) -> LinearPowerStripResult:
    if requested_power < 0:
        return LinearPowerStripResult(poly, 0, False)
    var quotient = poly.copy()
    var divisions = 0
    for _ in range(requested_power):
        var step = synthetic_divide_monic_linear(quotient, root)
        if step.remainder != 0:
            return LinearPowerStripResult(quotient, divisions, False)
        quotient = step.quotient.copy()
        divisions += 1
    var next = synthetic_divide_monic_linear(quotient, root)
    return LinearPowerStripResult(
        quotient, divisions, next.remainder != 0,
    )


def divide_monic_poly(poly: PolyZ, divisor: PolyZ) -> PolyDivisionResult:
    """Long division by a monic divisor over Z; exact iff the remainder is 0."""
    if divisor.coefficient(divisor.degree) != 1 or poly.degree < divisor.degree:
        return PolyDivisionResult(PolyZ(), False)
    var remainder = poly.copy()
    var quotient = PolyZ()
    for offset in range(poly.degree - divisor.degree + 1):
        var shift = poly.degree - divisor.degree - offset
        var lead = remainder.coefficient(shift + divisor.degree)
        quotient.coeffs[shift] = lead
        for i in range(divisor.degree + 1):
            remainder.coeffs[shift + i] -= lead * divisor.coefficient(i)
    quotient.normalize()
    remainder.normalize()
    return PolyDivisionResult(quotient, remainder.is_zero())


def expected_r31_cubic() -> PolyZ:
    # C^3+2C^2+2C+2, the non-rational factor of A_{3,1}.
    var cubic = PolyZ()
    cubic.coeffs[0] = 2
    cubic.coeffs[1] = 2
    cubic.coeffs[2] = 2
    cubic.coeffs[3] = 1
    cubic.normalize()
    return cubic^


def rejected_r41_residual_divisor_multiset() -> R41ResidualDivisorMultiset:
    return R41ResidualDivisorMultiset(
        0, 0, 0, 0, 0, 0,
        False, False, False, False, False, False, True,
    )


def verify_r41_residual_divisor_multiset() -> R41ResidualDivisorMultiset:
    var relation = raw_return_poly(4, 1)
    var strip_zero = strip_monic_linear_power(relation, 0, 5)
    if not strip_zero.exact:
        return rejected_r41_residual_divisor_multiset()
    var strip_minus_two = strip_monic_linear_power(
        strip_zero.quotient, -2, 1,
    )
    if not strip_minus_two.exact:
        return rejected_r41_residual_divisor_multiset()
    var cubic = expected_r31_cubic()
    var strip_cubic = divide_monic_poly(strip_minus_two.quotient, cubic)
    if not strip_cubic.exact:
        return rejected_r41_residual_divisor_multiset()
    var residual = strip_cubic.quotient.copy()
    var cubic_divides_r31 = divide_monic_poly(raw_return_poly(3, 1), cubic)
    var zero_is_exact_4_1 = integer_exact_minimal_collision_pattern(0, 4, 1)
    var minus_two_is_exact_4_1 = integer_exact_minimal_collision_pattern(
        -2, 4, 1,
    )
    var stripped = (
        strip_zero.divisions + strip_minus_two.divisions + cubic.degree
    )
    return R41ResidualDivisorMultiset(
        relation.degree,
        strip_zero.divisions,
        strip_minus_two.divisions,
        1,
        stripped,
        residual.degree,
        relation.degree == stripped + residual.degree,
        equal_poly(relation, expected_R_4_1_factorized()),
        equal_poly(residual, expected_F7_M41()),
        not zero_is_exact_4_1 and not minus_two_is_exact_4_1,
        cubic_divides_r31.exact,
        False,
        False,
    )


def critical_relation_residual_multiset_smoke() -> Bool:
    var result = verify_r41_residual_divisor_multiset()
    var invalid_power = strip_monic_linear_power(
        raw_return_poly(4, 1), 0, -1,
    )
    return (
        result.algebraic_replay_accepted() and
        not result.exact_type_divisor_accepted() and
        result.stripped_lower_type_multiplicity == 9 and
        result.residual_degree == 7 and
        not invalid_power.exact and
        not result.proves_density() and
        not result.proves_equidistribution() and
        not result.proves_c1()
    )
