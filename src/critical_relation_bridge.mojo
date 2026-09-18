# critical_relation_bridge.mojo
#
# First executable slice of docs/multiset-bridge-program.md.
#
# This checker proves a bounded modular statement about the integral
# critical-orbit relation A_{ell,k} = Q_{ell+k} - Q_ell.  Acceptance means:
# - the supplied modulus is prime;
# - polynomial reduction agrees with direct orbit iteration through ell+k;
# - the declared return relation holds;
# - every other collision through the minimal horizon is excluded; and
# - the critical-relation root is simple modulo p.
#
# It does not construct an infinite Hensel lift, identify a
# characteristic-zero factor, choose a complex embedding, or localize a
# parameter root.

from poly_z import PolyZ, critical_orbit_poly, derivative, sub

comptime MAX_BRIDGE_PRIME = 1048576
comptime MAX_BRIDGE_HORIZON = 8
comptime MAX_HENSEL_PRIME = 4096
comptime MAX_HENSEL_HORIZON = 6


struct SimpleResidueRootCertificate(ImplicitlyCopyable):
    var prime: Int
    var residue: Int
    var preperiod: Int
    var period: Int
    var reduction_commutes: Bool
    var relation_holds: Bool
    var exact_type_exclusions_hold: Bool
    var derivative_nonzero: Bool
    var rejected: Bool

    def __init__(
        out self,
        prime: Int,
        residue: Int,
        preperiod: Int,
        period: Int,
        reduction_commutes: Bool,
        relation_holds: Bool,
        exact_type_exclusions_hold: Bool,
        derivative_nonzero: Bool,
        rejected: Bool,
    ):
        self.prime = prime
        self.residue = residue
        self.preperiod = preperiod
        self.period = period
        self.reduction_commutes = reduction_commutes
        self.relation_holds = relation_holds
        self.exact_type_exclusions_hold = exact_type_exclusions_hold
        self.derivative_nonzero = derivative_nonzero
        self.rejected = rejected

    def accepted(self) -> Bool:
        return (
            not self.rejected and self.reduction_commutes and
            self.relation_holds and self.exact_type_exclusions_hold and
            self.derivative_nonzero
        )


struct HenselStepCertificate(ImplicitlyCopyable):
    """One independently replayable lift from a simple root modulo p to the
    unique compatible root modulo p^2."""

    var prime: Int
    var base_residue: Int
    var correction_digit: Int
    var lifted_residue: Int
    var modulus_squared: Int
    var base_certificate_accepted: Bool
    var congruent_to_base: Bool
    var lifted_relation_holds: Bool
    var derivative_unit: Bool
    var rejected: Bool

    def __init__(
        out self,
        prime: Int,
        base_residue: Int,
        correction_digit: Int,
        lifted_residue: Int,
        modulus_squared: Int,
        base_certificate_accepted: Bool,
        congruent_to_base: Bool,
        lifted_relation_holds: Bool,
        derivative_unit: Bool,
        rejected: Bool,
    ):
        self.prime = prime
        self.base_residue = base_residue
        self.correction_digit = correction_digit
        self.lifted_residue = lifted_residue
        self.modulus_squared = modulus_squared
        self.base_certificate_accepted = base_certificate_accepted
        self.congruent_to_base = congruent_to_base
        self.lifted_relation_holds = lifted_relation_holds
        self.derivative_unit = derivative_unit
        self.rejected = rejected

    def accepted(self) -> Bool:
        return (
            not self.rejected and self.base_certificate_accepted and
            self.congruent_to_base and self.lifted_relation_holds and
            self.derivative_unit
        )


def bridge_residue(value: Int, prime: Int) -> Int:
    var out = value % prime
    if out < 0:
        out += prime
    return out


def bounded_prime(prime: Int) -> Bool:
    if prime < 2 or prime > MAX_BRIDGE_PRIME:
        return False
    if prime == 2:
        return True
    if prime % 2 == 0:
        return False
    var divisor = 3
    while divisor <= prime // divisor:
        if prime % divisor == 0:
            return False
        divisor += 2
    return True


def eval_poly_mod(poly: PolyZ, value: Int, prime: Int) -> Int:
    var out = 0
    var x = bridge_residue(value, prime)
    for offset in range(poly.degree + 1):
        var index = poly.degree - offset
        out = bridge_residue(out * x + bridge_residue(poly.coefficient(index), prime), prime)
    return out


def inverse_mod_prime(value: Int, prime: Int) -> Int:
    """Extended Euclidean inverse; returns -1 when no inverse exists."""
    var old_r = prime
    var r = bridge_residue(value, prime)
    var old_t = 0
    var t = 1
    while r != 0:
        var quotient = old_r // r
        var next_r = old_r - quotient * r
        old_r = r
        r = next_r
        var next_t = old_t - quotient * t
        old_t = t
        t = next_t
    if old_r != 1:
        return -1
    return bridge_residue(old_t, prime)


def orbit_value_mod(parameter: Int, depth: Int, prime: Int) -> Int:
    var value = 0
    var c = bridge_residue(parameter, prime)
    for _ in range(depth):
        value = bridge_residue(value * value + c, prime)
    return value


def reduction_commutes_through(parameter: Int, horizon: Int, prime: Int) -> Bool:
    for depth in range(horizon + 1):
        var polynomial_value = eval_poly_mod(critical_orbit_poly(depth), parameter, prime)
        if polynomial_value != orbit_value_mod(parameter, depth, prime):
            return False
    return True


def exact_minimal_collision_pattern(parameter: Int, ell: Int, k: Int, prime: Int) -> Bool:
    var horizon = ell + k
    for left in range(horizon + 1):
        var left_value = orbit_value_mod(parameter, left, prime)
        for right in range(left + 1, horizon + 1):
            var equal = left_value == orbit_value_mod(parameter, right, prime)
            var intended = left == ell and right == horizon
            if equal != intended:
                return False
    return True


def rejected_simple_root_certificate() -> SimpleResidueRootCertificate:
    return SimpleResidueRootCertificate(0, 0, 0, 0, False, False, False, False, True)


def verify_simple_residue_root(
    parameter: Int, ell: Int, k: Int, prime: Int
) -> SimpleResidueRootCertificate:
    if (
        not bounded_prime(prime) or ell < 0 or k < 1 or
        ell + k > MAX_BRIDGE_HORIZON
    ):
        return rejected_simple_root_certificate()

    var q_later = critical_orbit_poly(ell + k)
    var q_earlier = critical_orbit_poly(ell)
    var relation = sub(q_later, q_earlier)
    var relation_derivative = derivative(relation)
    var residue = bridge_residue(parameter, prime)
    var commutes = reduction_commutes_through(residue, ell + k, prime)
    var relation_holds = eval_poly_mod(relation, residue, prime) == 0
    var exclusions = exact_minimal_collision_pattern(residue, ell, k, prime)
    var simple = eval_poly_mod(relation_derivative, residue, prime) != 0
    return SimpleResidueRootCertificate(
        prime,
        residue,
        ell,
        k,
        commutes,
        relation_holds,
        exclusions,
        simple,
        False,
    )


def rejected_hensel_step() -> HenselStepCertificate:
    return HenselStepCertificate(0, 0, 0, 0, 0, False, False, False, False, True)


def verify_hensel_step(
    parameter: Int, ell: Int, k: Int, prime: Int
) -> HenselStepCertificate:
    """Compute and replay the unique simple-root correction modulo p^2.

    This is one finite Hensel step. It is not an infinite p-adic lift and does
    not identify a characteristic-zero factor or complex embedding.
    """
    if prime > MAX_HENSEL_PRIME or ell + k > MAX_HENSEL_HORIZON:
        return rejected_hensel_step()
    var base = verify_simple_residue_root(parameter, ell, k, prime)
    if not base.accepted():
        return rejected_hensel_step()
    var relation = sub(critical_orbit_poly(ell + k), critical_orbit_poly(ell))
    var relation_derivative = derivative(relation)
    var modulus_squared = prime * prime
    var relation_at_base = eval_poly_mod(relation, base.residue, modulus_squared)
    if relation_at_base % prime != 0:
        return rejected_hensel_step()
    var quotient_mod_prime = (relation_at_base // prime) % prime
    var derivative_mod_prime = eval_poly_mod(relation_derivative, base.residue, prime)
    var inverse = inverse_mod_prime(derivative_mod_prime, prime)
    if inverse < 0:
        return rejected_hensel_step()
    var correction = bridge_residue(-quotient_mod_prime * inverse, prime)
    var lifted = base.residue + prime * correction
    var congruent = lifted % prime == base.residue
    var lifted_relation = eval_poly_mod(relation, lifted, modulus_squared) == 0
    return HenselStepCertificate(
        prime,
        base.residue,
        correction,
        lifted,
        modulus_squared,
        base.accepted(),
        congruent,
        lifted_relation,
        derivative_mod_prime != 0,
        False,
    )


def critical_relation_bridge_smoke() -> Bool:
    # c = -2 reduces to 3 modulo 5 and has orbit 0,3,2,2: exact type (2,1).
    # A_{2,1}(C) = C^3(C+2); the root 3 is simple modulo 5.
    var accepted = verify_simple_residue_root(-2, 2, 1, 5)
    var repeated = verify_simple_residue_root(0, 2, 1, 5)
    var composite = verify_simple_residue_root(3, 2, 1, 9)
    var wrong_type = verify_simple_residue_root(3, 1, 1, 5)
    var lift = verify_hensel_step(-2, 2, 1, 5)
    var refused_lift = verify_hensel_step(0, 2, 1, 5)
    return (
        accepted.accepted() and accepted.residue == 3 and
        not repeated.accepted() and repeated.relation_holds and
        not repeated.derivative_nonzero and
        not composite.accepted() and composite.rejected and
        not wrong_type.accepted() and
        lift.accepted() and lift.base_residue == 3 and
        lift.correction_digit == 4 and lift.lifted_residue == 23 and
        lift.modulus_squared == 25 and
        not refused_lift.accepted() and refused_lift.rejected
    )
