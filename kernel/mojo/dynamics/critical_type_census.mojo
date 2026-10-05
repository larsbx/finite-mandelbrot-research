# critical_type_census.mojo
#
# The exact critical-orbit type modulo p, read from the vendored
# `finite_field_orbit` census (contract orbit-census-v1, pinned in
# vendored.toml), and the modular obstruction it yields.
#
# Write z_0 = 0, z_{n+1} = z_n^2 + c.  The type of c modulo p is (mu, lambda):
# z_{mu+lambda} is the first term equal to an earlier one, and z_mu is that
# earlier term.  The single-seed census block (p, c mod p, cap, 0, 1) answers it
# exactly, resolved iff mu + lambda <= cap.
#
# Obstruction.  If c is an integer whose critical orbit has exact type
# (ell, k) over Q, then z_{ell+k} = z_ell, so z_{ell+k} = z_ell modulo every
# p, and that holds iff mu <= ell and lambda divides k.  One prime where it
# fails excludes the type (ell, k) for c.  The converse does not hold: a type
# unobstructed at every prime tried is not thereby the exact type over Q.
#
# The bounded bridge check `exact_minimal_collision_pattern(c, ell, k, p)`
# says the same thing as "the type modulo p is (ell, k)"; the smoke below
# checks that equivalence, and the obstruction against direct iteration, on
# every residue of the small primes through horizon MAX_BRIDGE_HORIZON.

from finite_field_orbit.census import Block, census
from dynamics.critical_relation_bridge import (
    MAX_BRIDGE_HORIZON,
    bridge_residue,
    exact_minimal_collision_pattern,
    orbit_value_mod,
)


@fieldwise_init
struct CriticalType(ImplicitlyCopyable):
    var resolved: Bool
    var mu: Int
    var period: Int

    def equals(self, ell: Int, k: Int) -> Bool:
        return self.resolved and self.mu == ell and self.period == k


def critical_type_mod_p(parameter: Int, prime: Int, cap: Int) raises -> CriticalType:
    """The census of seed 0; raises the contract's refusal for a malformed block."""
    var a = census(Block(prime, bridge_residue(parameter, prime), cap, 0, 1))
    return CriticalType(a.resolved == 1, a.w_mu, a.w_lambda)


def type_obstructed_mod_p(parameter: Int, ell: Int, k: Int, prime: Int) raises -> Bool:
    """True iff p excludes exact type (ell, k), k >= 1, for the integer parameter."""
    var t = critical_type_mod_p(parameter, prime, ell + k)
    return not (t.resolved and t.mu <= ell and k % t.period == 0)


def census_agrees_with_the_bridge() raises -> Bool:
    # c = -2 has orbit 0, -2, 2, 2: exact type (2, 1), unobstructed at every p.
    # c = 1 has orbit 0, 1, 2, 5, ...; modulo 2 it is 0, 1, 0, so (2, 1) fails.
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if type_obstructed_mod_p(-2, 2, 1, prime):
            return False
        for c in range(prime):
            for horizon in range(1, MAX_BRIDGE_HORIZON + 1):
                var t = critical_type_mod_p(c, prime, horizon)
                for k in range(1, horizon + 1):
                    var ell = horizon - k
                    if t.equals(ell, k) != exact_minimal_collision_pattern(c, ell, k, prime):
                        return False
                    var returns = orbit_value_mod(c, horizon, prime) == orbit_value_mod(c, ell, prime)
                    if type_obstructed_mod_p(c, ell, k, prime) == returns:
                        return False
    return type_obstructed_mod_p(1, 2, 1, 2) and not type_obstructed_mod_p(-1, 0, 2, 1048573)


def critical_type_census_smoke() -> Bool:
    try:
        return census_agrees_with_the_bridge()
    except:
        return False
