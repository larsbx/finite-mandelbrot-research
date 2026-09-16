# C1 separated-pair density: the exact angle measure of the pairs a finite
# separator-catalogue prefix already decides.
# This file is terminology-governed by docs/C1_separated_pair_density.md.
# Arithmetic specification: docs/rational-interval-arithmetic-spec.md (binding row
# "finite angle-measure density"): every length, square, and sum is an unbounded
# exact rational; rejection is sticky and no floating point appears.
#
# A catalogue prefix contributes finitely many rational ray addresses. Those
# cut the external-angle circle into finitely many arcs; two parameters whose
# angles lie in different arcs are separated at that prefix. The density is
# the measure of the separated pairs under the product of Lebesgue measure on
# angles, computed exactly over unbounded rationals:
#
#   density(k) = 1 - sum_j |I_j|^2,     residue(k) = sum_j |I_j|^2.
#
# It is the parameter-space analogue of the common fraction `f_m` of the PSC
# overlap route. Nothing here decides a named pair: a residue tending to zero
# would make the undecided pairs null, never empty, which is exactly the leak
# of the theorem tag `HarmonicMeasureAlmostEveryFibreTrivial` in
# src/C1_theorem_tag_import_ledger.mojo.

from checked_ray_address import make_checked_ray_addr
from finite_exact.rat_q import Q


struct SeparatedDensityResult(ImplicitlyCopyable):
    """`density` and `residue` sum to one; `arcs` is the number of arcs the
    distinct cuts induce. A rejected result carries no measure."""

    var density: Q
    var residue: Q
    var arcs: Int
    var rejected: Bool

    def __init__(out self, density: Q, residue: Q, arcs: Int, rejected: Bool):
        self.density = density
        self.residue = residue
        self.arcs = arcs
        self.rejected = rejected

    def accepted(self) -> Bool:
        return not self.rejected


def rejected_density() -> SeparatedDensityResult:
    return SeparatedDensityResult(Q.zero(), Q.zero(), 0, True)


def _sorted_distinct_cuts(nums: List[Int64], dens: List[Int64]) raises -> List[Q]:
    """The cut angles as normalized exact rationals in `[0, 1)`, ascending and
    without repetition. Raises on a malformed address."""
    var out = List[Q]()
    for i in range(len(nums)):
        var addr = make_checked_ray_addr(nums[i], dens[i])
        if addr.rejected:
            raise Error("cut angle is not a normalized ray address")
        var value = Q(addr.num, addr.den)
        if not value.accepted():
            raise Error("cut angle is not an accepted rational")
        var at = len(out)
        var duplicate = False
        for j in range(len(out)):
            if value.eq(out[j]):
                duplicate = True
                break
            if value.lt(out[j]):
                at = j
                break
        if duplicate:
            continue
        var next = List[Q]()
        for j in range(at):
            next.append(out[j].copy())
        next.append(value.copy())
        for j in range(at, len(out)):
            next.append(out[j].copy())
        out = next^
    return out^


# Regime correspondence: separated-pair-density
def separated_pair_density(nums: List[Int64], dens: List[Int64]) -> SeparatedDensityResult:
    """Exact density of the pairs the cuts separate. Fails closed on a length
    mismatch, a malformed address, or arcs whose exact lengths do not sum to
    one (which no accepted input can produce, so it is a kernel self-check)."""
    if len(nums) != len(dens):
        return rejected_density()
    try:
        var cuts = _sorted_distinct_cuts(nums, dens)
        var count = len(cuts)
        if count < 2:
            # No cut, or one cut: the circle is a single arc and no pair is decided.
            return SeparatedDensityResult(Q.zero(), Q.one(), 1, False)
        var total = Q.zero()
        var residue = Q.zero()
        for j in range(count):
            var length = Q.zero()
            if j == count - 1:
                length = Q.one().sub(cuts[count - 1]).add(cuts[0])
            else:
                length = cuts[j + 1].sub(cuts[j])
            if not length.accepted():
                return rejected_density()
            total = total.add(length)
            residue = residue.add(length.square())
        if not (total.accepted() and total.eq(Q.one())):
            return rejected_density()
        var density = Q.one().sub(residue)
        if not (density.accepted() and residue.accepted()):
            return rejected_density()
        return SeparatedDensityResult(density, residue, count, False)
    except:
        return rejected_density()


# --- non-claims ---------------------------------------------------------------


def density_one_implies_every_pair_separated() -> Bool:
    # A null set of undecided pairs is not an empty one. The infinitely
    # renormalizable parameters of docs/C1_residual_directive_carrier.md are
    # the standing example.
    return False


def finite_prefix_density_decides_persistent_non_separation() -> Bool:
    return False


def density_is_harmonic_measure_of_the_boundary() -> Bool:
    # The measure here is Lebesgue measure on external angles, pushed to pairs.
    # Identifying it with harmonic measure on the boundary of M is the imported
    # theorem tag's business, under that tag's hypotheses.
    return False


# --- smoke ------------------------------------------------------------------------


def _density(nums: List[Int64], dens: List[Int64]) -> SeparatedDensityResult:
    return separated_pair_density(nums, dens)


def _is(result: SeparatedDensityResult, num: Int64, den: Int64) -> Bool:
    return result.accepted() and result.density.eq(Q(num, den))


def separated_density_smoke() -> Bool:
    # Two rays of one separator: arcs 1/3 and 2/3, so 2 * (1/3) * (2/3) of pairs.
    var thirds_n: List[Int64] = [1, 2]
    var thirds_d: List[Int64] = [3, 3]
    var thirds = _density(thirds_n, thirds_d)
    if not (_is(thirds, 4, 9) and thirds.arcs == 2 and thirds.residue.eq(Q(5, 9))):
        return False
    # The rabbit wake addresses: arcs 1/7, 2/7, 4/7.
    var rabbit_n: List[Int64] = [1, 2, 4]
    var rabbit_d: List[Int64] = [7, 7, 7]
    var rabbit = _density(rabbit_n, rabbit_d)
    if not (_is(rabbit, 4, 7) and rabbit.arcs == 3 and rabbit.residue.eq(Q(3, 7))):
        return False
    # Refinement never lowers the density: adding the cut 0 to {1/3, 2/3}.
    var refined_n: List[Int64] = [0, 1, 2]
    var refined_d: List[Int64] = [1, 3, 3]
    var refined = _density(refined_n, refined_d)
    if not (_is(refined, 2, 3) and refined.arcs == 3):
        return False
    if not thirds.density.lt(refined.density):
        return False
    # Repetition is not refinement.
    var repeated_n: List[Int64] = [1, 2, 1]
    var repeated_d: List[Int64] = [3, 3, 3]
    var repeated = _density(repeated_n, repeated_d)
    if not (_is(repeated, 4, 9) and repeated.arcs == 2):
        return False
    # Fewer than two distinct cuts decide nothing.
    var empty = _density(List[Int64](), List[Int64]())
    var single_n: List[Int64] = [1]
    var single_d: List[Int64] = [3]
    var single = _density(single_n, single_d)
    if not (_is(empty, 0, 1) and empty.arcs == 1 and _is(single, 0, 1) and single.arcs == 1):
        return False
    if not (empty.residue.eq(Q.one()) and single.residue.eq(Q.one())):
        return False
    # Fail closed: malformed address, out-of-range address, length mismatch.
    var bad_n: List[Int64] = [1, 1]
    var bad_d: List[Int64] = [3, 0]
    var over_n: List[Int64] = [1, 7]
    var over_d: List[Int64] = [3, 5]
    var short_d: List[Int64] = [3]
    if _density(bad_n, bad_d).accepted() or _density(over_n, over_d).accepted():
        return False
    if _density(bad_n, short_d).accepted():
        return False
    return (
        not density_one_implies_every_pair_separated()
        and not finite_prefix_density_decides_persistent_non_separation()
        and not density_is_harmonic_measure_of_the_boundary()
    )
