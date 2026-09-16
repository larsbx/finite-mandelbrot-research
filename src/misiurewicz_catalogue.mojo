# Exact-type catalogue of Misiurewicz ray addresses (round-one item B6).
# This file is terminology-governed by docs/C1_misiurewicz_catalogue.md; the
# term `exact-type catalogue` is registered in docs/terminology-registry.md.
#
# A rational ray address `p/q` in lowest terms has, under doubling modulo one,
# an exact preperiod and an exact period read off `q` alone: write `q = 2^l m`
# with `m` odd, and the address has preperiod `l` and period the multiplicative
# order of `2` modulo `m`, with `m = 1` giving period one because zero is
# fixed. An address is of Misiurewicz type when `l >= 1`: the orbit is strictly
# preperiodic.
#
# The catalogue of exact type `(l, k)` is the finite set of such addresses. Its
# size obeys the counting identity
#
#   count(l, k) = 2^(l-1) * sum_{d | k} mu(k/d) (2^d - 1),
#
# because the addresses of exact type `(l, k)` are exactly `p / (2^l m)` in
# lowest terms with `m` odd of multiplicative order `k`, of which there are
# `phi(2^l m) = 2^(l-1) phi(m)`, and the orders sum by Moebius inversion over
# the divisors of `2^k - 1`. `catalogue_matches_count` checks the identity
# against the enumeration, which is the round-one angle-count regression.
#
# All arithmetic is fixed-width integer arithmetic bounded before use: types
# beyond `MAX_TYPE_INDEX` and denominators beyond `MAX_CATALOGUE_DENOMINATOR`
# are refused rather than computed, so nothing here can overflow. No floating
# point and no measured angle appears; these are finite symbolic addresses.
#
# Scope: the catalogue is a finite set of addresses. It is not a set of
# parameters, it locates nothing in the plane, and the triviality of the
# fibres of the corresponding parameters is the imported theorem tag
# `KnownTrivialFiberClass`, not a property computed here.

from integer_gcd import gcd_int

comptime MAX_TYPE_INDEX = 20
comptime MAX_CATALOGUE_DENOMINATOR = 1048576


struct MisiurewiczType(ImplicitlyCopyable):
    """`preperiod` and `period` of a ray address under doubling; a rejected
    value carries no type."""

    var preperiod: Int
    var period: Int
    var rejected: Bool

    def __init__(out self, preperiod: Int, period: Int, rejected: Bool):
        self.preperiod = preperiod
        self.period = period
        self.rejected = rejected

    def accepted(self) -> Bool:
        return not self.rejected

    def misiurewicz(self) -> Bool:
        """Strictly preperiodic: the orbit never returns to the address."""
        return self.accepted() and self.preperiod >= 1


def rejected_type() -> MisiurewiczType:
    return MisiurewiczType(0, 0, True)


# Regime correspondence: misiurewicz-exact-type
def exact_type(num: Int, den: Int) -> MisiurewiczType:
    """Exact preperiod and period of `num/den` under doubling modulo one.
    Refuses an address outside `[0, 1)`, a non-positive denominator, and a
    denominator beyond the catalogue bound."""
    if den <= 0 or num < 0 or num >= den or den > MAX_CATALOGUE_DENOMINATOR:
        return rejected_type()
    var divisor = gcd_int(num, den)
    if divisor <= 0:
        return rejected_type()
    var reduced = den // divisor
    var preperiod = 0
    while reduced % 2 == 0:
        reduced = reduced // 2
        preperiod += 1
    if reduced == 1:
        # A dyadic address falls onto the fixed point zero.
        return MisiurewiczType(preperiod, 1, False)
    var period = 1
    var power = 2 % reduced
    while power != 1:
        power = (power * 2) % reduced
        period += 1
        if period > reduced:
            return rejected_type()
    return MisiurewiczType(preperiod, period, False)


def moebius(n: Int) -> Int:
    """`mu(n)` for `n >= 1`: zero on a squareful argument, else the sign of the
    number of prime factors. Returns zero for `n < 1`, which no caller passes."""
    if n < 1:
        return 0
    var rest = n
    var sign = 1
    var factor = 2
    while factor * factor <= rest:
        if rest % factor == 0:
            rest = rest // factor
            if rest % factor == 0:
                return 0
            sign = -sign
        factor += 1
    if rest > 1:
        sign = -sign
    return sign


def catalogue_denominator(preperiod: Int, period: Int) -> Int:
    """`2^l (2^k - 1)`, the common denominator of every address of exact type
    `(l, k)`. Returns `-1` when the type is out of range or the denominator
    exceeds the catalogue bound."""
    if preperiod < 1 or period < 1 or preperiod > MAX_TYPE_INDEX or period > MAX_TYPE_INDEX:
        return -1
    var odd_part = (1 << period) - 1
    var scale = 1 << preperiod
    if odd_part > MAX_CATALOGUE_DENOMINATOR // scale:
        return -1
    return scale * odd_part


# Regime correspondence: misiurewicz-exact-type
def catalogue_count(preperiod: Int, period: Int) -> Int:
    """`2^(l-1) sum_{d | k} mu(k/d) (2^d - 1)`, the size the identity predicts.
    Returns `-1` for a type out of range."""
    if catalogue_denominator(preperiod, period) < 0:
        return -1
    var total = 0
    for d in range(1, period + 1):
        if period % d == 0:
            total += moebius(period // d) * ((1 << d) - 1)
    return (1 << (preperiod - 1)) * total


# Regime correspondence: misiurewicz-exact-type
def catalogue(preperiod: Int, period: Int) -> List[Int]:
    """Numerators, ascending, of every address of exact type `(l, k)` over the
    denominator `catalogue_denominator(l, k)`. Empty for a type out of range."""
    var out = List[Int]()
    var den = catalogue_denominator(preperiod, period)
    if den < 0:
        return out^
    for num in range(den):
        var found = exact_type(num, den)
        if found.accepted() and found.preperiod == preperiod and found.period == period:
            out.append(num)
    return out^


def catalogue_matches_count(preperiod: Int, period: Int) -> Bool:
    """The angle-count regression: enumeration agrees with the identity."""
    var den = catalogue_denominator(preperiod, period)
    if den < 0:
        return False
    return len(catalogue(preperiod, period)) == catalogue_count(preperiod, period)


# --- non-claims ---------------------------------------------------------------


def catalogue_is_a_set_of_parameters() -> Bool:
    # The catalogue holds ray addresses. Associating a parameter with an address
    # needs a landing theorem tag and an adapter, neither of which is here.
    return False


def catalogue_proves_fibre_triviality() -> Bool:
    # Triviality of the fibres of Misiurewicz parameters is the imported tag
    # KnownTrivialFiberClass, under its own hypotheses.
    return False


# --- smoke ------------------------------------------------------------------------


def _same(a: List[Int], b: List[Int]) -> Bool:
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def misiurewicz_catalogue_smoke() -> Bool:
    # 1/2 -> 0 -> 0: preperiod one, period one, and Misiurewicz.
    var half = exact_type(1, 2)
    if not (half.misiurewicz() and half.preperiod == 1 and half.period == 1):
        return False
    # 1/6 -> 1/3 -> 2/3 -> 1/3: preperiod one, period two.
    var sixth = exact_type(1, 6)
    if not (sixth.misiurewicz() and sixth.preperiod == 1 and sixth.period == 2):
        return False
    # 1/3 is periodic, so it is not of Misiurewicz type.
    var third = exact_type(1, 3)
    if not (third.accepted() and third.preperiod == 0 and third.period == 2):
        return False
    if third.misiurewicz():
        return False
    # Reduction first: 2/6 is 1/3, not an address of preperiod one.
    var reducible = exact_type(2, 6)
    if not (reducible.accepted() and reducible.preperiod == 0 and reducible.period == 2):
        return False
    # The pinned catalogues.
    var one_one: List[Int] = [1]
    var two_one: List[Int] = [1, 3]
    var one_two: List[Int] = [1, 5]
    var one_three: List[Int] = [1, 3, 5, 9, 11, 13]
    if not _same(catalogue(1, 1), one_one) or catalogue_denominator(1, 1) != 2:
        return False
    if not _same(catalogue(2, 1), two_one) or catalogue_denominator(2, 1) != 4:
        return False
    if not _same(catalogue(1, 2), one_two) or catalogue_denominator(1, 2) != 6:
        return False
    if not _same(catalogue(1, 3), one_three) or catalogue_denominator(1, 3) != 14:
        return False
    # The counting identity against the enumeration.
    for l in range(1, 5):
        for k in range(1, 5):
            if not catalogue_matches_count(l, k):
                return False
    if catalogue_count(1, 1) != 1 or catalogue_count(2, 3) != 12 or catalogue_count(3, 3) != 24:
        return False
    # Moebius values the identity relies on.
    if moebius(1) != 1 or moebius(2) != -1 or moebius(4) != 0 or moebius(6) != 1 or moebius(30) != -1:
        return False
    # Fail closed: out-of-range addresses, types, and denominators.
    if exact_type(1, 0).accepted() or exact_type(5, 3).accepted() or exact_type(-1, 4).accepted():
        return False
    if catalogue_denominator(0, 2) >= 0 or catalogue_denominator(1, 0) >= 0:
        return False
    if catalogue_denominator(1, MAX_TYPE_INDEX + 1) >= 0 or catalogue_denominator(1, 20) >= 0:
        return False
    if catalogue_count(0, 1) != -1 or len(catalogue(0, 1)) != 0:
        return False
    return not catalogue_is_a_set_of_parameters() and not catalogue_proves_fibre_triviality()
