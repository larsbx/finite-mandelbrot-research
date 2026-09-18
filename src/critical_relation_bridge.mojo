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
# It does not construct a Hensel lift, identify a characteristic-zero factor,
# choose a complex embedding, or localize a parameter root.

from poly_z import PolyZ, critical_orbit_poly, derivative, sub

comptime MAX_BRIDGE_PRIME = 1048576
comptime MAX_BRIDGE_HORIZON = 8


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


def critical_relation_bridge_smoke() -> Bool:
    # c = -2 reduces to 3 modulo 5 and has orbit 0,3,2,2: exact type (2,1).
    # A_{2,1}(C) = C^3(C+2); the root 3 is simple modulo 5.
    var accepted = verify_simple_residue_root(-2, 2, 1, 5)
    var repeated = verify_simple_residue_root(0, 2, 1, 5)
    var composite = verify_simple_residue_root(3, 2, 1, 9)
    var wrong_type = verify_simple_residue_root(3, 1, 1, 5)
    return (
        accepted.accepted() and accepted.residue == 3 and
        not repeated.accepted() and repeated.relation_holds and
        not repeated.derivative_nonzero and
        not composite.accepted() and composite.rejected and
        not wrong_type.accepted()
    )
