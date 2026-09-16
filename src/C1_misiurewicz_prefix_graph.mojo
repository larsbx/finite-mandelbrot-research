# C1 obstruction extractor on Misiurewicz prefix graphs (round-two item R5).
# This file is terminology-governed by docs/C1_misiurewicz_prefix_graph.md; the
# term `prefix obstruction` is registered in docs/terminology-registry.md.
#
# Route F1 of docs/C1_F1_obstruction_extraction.md asks for a finite obstruction
# object that a rational-ray catalogue can see. The overlap route of
# larsbx/pisot-substitution-conjecture-research already extracts one on a finite
# graph (docs/p1-overlap-minimal-obstruction-2026-09-14.md,
# mojo/psc/overlap_obstruction.mojo). This runs the same pipeline on the graphs
# the exact-type catalogue of src/misiurewicz_catalogue.mojo supplies:
#
#   vertices      the forward orbit closure of a catalogue under doubling
#   pairs         the unordered non-diagonal pairs of vertices
#   productive    separated by the prefix now, or with a productive successor
#   nonproductive the rest: the pairs no iterate ever separates
#   sinks         the cycles of the nonproductive set
#   dichotomy     each cycle is a boundary or an interior obstruction
#
# Productivity is computed backwards from the separated pairs, exactly as the
# overlap route computes it backwards from the coincidences. Forward closedness
# of the nonproductive set is then a lemma, not a computation: a nonproductive
# pair cannot have a productive successor, because a separation reached from the
# successor is reached from the pair one step earlier.
#
# Doubling is a function, so the pair graph has out-degree at most one and each
# component falls into exactly one cycle. The sink components are therefore the
# cycles, and no strongly-connected-component search is needed; this is where
# the mirror is simpler than the overlap route, whose graph branches.
#
# A merging pair, whose two points share an image, has no successor and is never
# separated, so it is nonproductive. Counting it productive would be the
# substantive error: those two addresses are precisely the ones doubling can
# never tell apart. They are transient, never sinks, and are counted separately.
#
# The dichotomy transfers term by term from the overlap route. A cycle is a
# boundary obstruction when some point on it is a separator endpoint, so the
# object may lie on the separation line itself: the `BoundaryEqualityCandidate`
# of docs/C1_canonical_carrier_content.md and the aligned obstruction of the
# overlap route, where a child start coincides. Otherwise it is an interior
# obstruction: no separator boundary is ever hit, which is `CarrierTooCoarse`
# and the strict-zipper case, where one side advances at every step.
#
# Bounds and fail-closed behaviour: one constant governs the graph. Vertices
# live in `Z/den`, so `MAX_PREFIX_GRAPH_DENOMINATOR` caps the vertex count and
# the pair count together. A denominator past it, a malformed separator, and an
# out-of-range point are refused rather than computed. Rejection is sticky and
# is never an empty answer: an empty obstruction set is a positive verdict about
# a complete graph, so a bounded search that failed must not read as one. That
# is UW-2: a bounded failed search is not persistent evidence.
#
# Scope: this decides one prefix. It does not decide persistent non-separation,
# which quantifies over every prefix, and an empty obstruction set is not fibre
# triviality, which for this class is the imported tag `KnownTrivialFiberClass`.
# No PF-critical or full-rank check appears here, for the same reason it appears
# nowhere in the overlap route: those are proved invariants of the output, not
# filters this code applies.

from misiurewicz_catalogue import catalogue, catalogue_denominator

comptime MAX_PREFIX_GRAPH_DENOMINATOR = 256


struct PrefixExtraction(Copyable, Movable):
    """The result of one extraction. `boundary` and `interior` count sink cycles
    by the dichotomy; `merging` counts the nonproductive pairs whose two points
    share an image. A rejected extraction carries no counts."""

    var vertices: Int
    var undecided: Int
    var nonproductive: Int
    var merging: Int
    var boundary: Int
    var interior: Int
    var rejected: Bool

    def __init__(out self, vertices: Int, undecided: Int, nonproductive: Int,
                 merging: Int, boundary: Int, interior: Int, rejected: Bool):
        self.vertices = vertices
        self.undecided = undecided
        self.nonproductive = nonproductive
        self.merging = merging
        self.boundary = boundary
        self.interior = interior
        self.rejected = rejected

    def accepted(self) -> Bool:
        return not self.rejected

    def cycles(self) -> Int:
        return self.boundary + self.interior

    def obstruction_free(self) -> Bool:
        """No pair survives doubling undecided. Only an accepted extraction can
        be obstruction free, and the test is the whole nonproductive set rather
        than its sinks, because a merging pair is nonproductive without lying on
        any cycle."""
        return self.accepted() and self.nonproductive == 0


def rejected_extraction() -> PrefixExtraction:
    return PrefixExtraction(0, 0, 0, 0, 0, 0, True)


# --- the finite objects ---------------------------------------------------------


# Regime correspondence: misiurewicz-prefix-obstruction
def forward_closure(seed: List[Int], den: Int) -> List[Int]:
    """The forward orbit closure of `seed` under doubling in `Z/den`, ascending.
    Empty when the denominator is past the bound or a point is out of range."""
    var out = List[Int]()
    if den <= 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR or len(seed) == 0:
        return out^
    var present = List[Bool]()
    for _ in range(den):
        present.append(False)
    for i in range(len(seed)):
        if seed[i] < 0 or seed[i] >= den:
            return List[Int]()
        present[seed[i]] = True
    # Doubling maps Z/den into itself, so one sweep to a fixpoint suffices and
    # the loop below runs at most den times.
    var changed = True
    while changed:
        changed = False
        for point in range(den):
            if present[point]:
                var image = (2 * point) % den
                if not present[image]:
                    present[image] = True
                    changed = True
    for point in range(den):
        if present[point]:
            out.append(point)
    return out^


def side(point: Int, low: Int, high: Int, den: Int) -> Int:
    """Which side of the two-ray separator `(low, high)` a point falls on: `1` on
    the arc running counterclockwise from the first ray to the second, `0` on the
    complement. Exchanging the two rays names the complementary side."""
    var offset = ((point - low) % den + den) % den
    var width = ((high - low) % den + den) % den
    if offset < width:
        return 1
    return 0


def separated(a: Int, b: Int, lows: List[Int], highs: List[Int], den: Int) -> Bool:
    """Separated by the prefix exactly when some separator puts the two points on
    opposite sides, that is when their side signatures differ."""
    for i in range(len(lows)):
        if side(a, lows[i], highs[i], den) != side(b, lows[i], highs[i], den):
            return True
    return False


def hits_endpoint(point: Int, lows: List[Int], highs: List[Int]) -> Bool:
    for i in range(len(lows)):
        if point == lows[i] or point == highs[i]:
            return True
    return False


def _code(a: Int, b: Int, den: Int) -> Int:
    """A pair is stored as one Int so the graph needs no nested lists. The lower
    point comes first, so each unordered pair has exactly one code."""
    if a < b:
        return a * den + b
    return b * den + a


def _successor_code(code: Int, den: Int) -> Int:
    """The image of a pair under doubling, or `-1` when the two points merge."""
    var a = (2 * (code // den)) % den
    var b = (2 * (code % den)) % den
    if a == b:
        return -1
    return _code(a, b, den)


# --- the extractor --------------------------------------------------------------


# Regime correspondence: misiurewicz-prefix-obstruction
def extract(seed: List[Int], lows: List[Int], highs: List[Int], den: Int) -> PrefixExtraction:
    """Run the pipeline on the forward closure of `seed` in `Z/den`. Fails closed
    on a mismatched or malformed separator list, an out-of-range point, and a
    denominator past the bound."""
    if den <= 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR or len(seed) == 0:
        return rejected_extraction()
    if len(lows) != len(highs):
        return rejected_extraction()
    for i in range(len(lows)):
        if lows[i] < 0 or highs[i] < 0 or lows[i] >= den or highs[i] >= den:
            return rejected_extraction()
        if lows[i] == highs[i]:
            return rejected_extraction()
    var vertices = forward_closure(seed, den)
    if len(vertices) == 0:
        return rejected_extraction()

    # Every unordered non-diagonal pair of vertices, with the productive ones
    # seeded from the pairs the prefix already separates.
    var codes = List[Int]()
    var productive = List[Bool]()
    for _ in range(den * den):
        productive.append(False)
    var is_pair = List[Bool]()
    for _ in range(den * den):
        is_pair.append(False)
    var undecided = 0
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            var code = _code(vertices[i], vertices[j], den)
            codes.append(code)
            is_pair[code] = True
            if separated(vertices[i], vertices[j], lows, highs, den):
                productive[code] = True
            else:
                undecided += 1

    # Productivity backwards from the separated pairs, to a fixpoint. A merging
    # pair has no successor, so it never becomes productive.
    var changed = True
    while changed:
        changed = False
        for i in range(len(codes)):
            var code = codes[i]
            if not productive[code]:
                var image = _successor_code(code, den)
                if image >= 0 and productive[image]:
                    productive[code] = True
                    changed = True

    # The nonproductive set, its merging pairs, and its sink cycles.
    var nonproductive = 0
    var merging = 0
    for i in range(len(codes)):
        if not productive[codes[i]]:
            nonproductive += 1
            if _successor_code(codes[i], den) < 0:
                merging += 1

    var seen = List[Bool]()
    var on_walk = List[Bool]()
    for _ in range(den * den):
        seen.append(False)
        on_walk.append(False)
    var boundary = 0
    var interior = 0
    for i in range(len(codes)):
        var start = codes[i]
        if productive[start] or seen[start]:
            continue
        # Walk forward. Doubling is a function, so the walk either leaves the
        # nonproductive set or closes into the unique cycle of this component.
        # `on_walk` is allocated once and cleared entry by entry below, so the
        # whole classification stays linear in the number of pairs.
        var walk = List[Int]()
        var point = start
        while point >= 0 and is_pair[point] and not productive[point] and not on_walk[point]:
            walk.append(point)
            on_walk[point] = True
            point = _successor_code(point, den)
        var closed = point >= 0 and on_walk[point]
        var found_new = closed and not seen[point]
        for k in range(len(walk)):
            seen[walk[k]] = True
            on_walk[walk[k]] = False
        if found_new:
            # Classify the cycle: it starts where the walk met itself.
            var at = 0
            for k in range(len(walk)):
                if walk[k] == point:
                    at = k
            var touches = False
            for k in range(at, len(walk)):
                var pair_code = walk[k]
                if hits_endpoint(pair_code // den, lows, highs):
                    touches = True
                if hits_endpoint(pair_code % den, lows, highs):
                    touches = True
            if touches:
                boundary += 1
            else:
                interior += 1

    return PrefixExtraction(len(vertices), undecided, nonproductive, merging,
                            boundary, interior, False)


def catalogue_separator_lows(preperiod: Int, period: Int) -> List[Int]:
    """The full separator prefix of an exact type pairs consecutive points of the
    forward closure; this is its list of first rays."""
    var out = List[Int]()
    var den = catalogue_denominator(preperiod, period)
    if den < 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR:
        return out^
    var vertices = forward_closure(catalogue(preperiod, period), den)
    if len(vertices) < 2:
        return out^
    for i in range(len(vertices)):
        out.append(vertices[i])
    return out^


def catalogue_separator_highs(preperiod: Int, period: Int) -> List[Int]:
    """The matching list of second rays."""
    var out = List[Int]()
    var den = catalogue_denominator(preperiod, period)
    if den < 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR:
        return out^
    var vertices = forward_closure(catalogue(preperiod, period), den)
    if len(vertices) < 2:
        return out^
    for i in range(len(vertices)):
        out.append(vertices[(i + 1) % len(vertices)])
    return out^


# Regime correspondence: misiurewicz-prefix-obstruction
def extract_catalogue(preperiod: Int, period: Int) -> PrefixExtraction:
    """The extractor on an exact type with its full separator prefix: the
    negative control this module exists to run."""
    var den = catalogue_denominator(preperiod, period)
    if den < 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR:
        return rejected_extraction()
    return extract(catalogue(preperiod, period),
                   catalogue_separator_lows(preperiod, period),
                   catalogue_separator_highs(preperiod, period), den)


# --- non-claims ---------------------------------------------------------------


def obstruction_free_proves_fibre_triviality() -> Bool:
    # An empty obstruction set is a fact about one finite prefix graph. Fibre
    # triviality for this class is the imported tag KnownTrivialFiberClass.
    return False


def extractor_decides_persistent_nonseparation() -> Bool:
    # Persistent non-separation quantifies over every prefix. This runs one.
    return False


def bounded_refusal_is_evidence_of_no_obstruction() -> Bool:
    # UW-2. A rejected extraction says nothing either way, which is why
    # obstruction_free() requires acceptance.
    return False


# --- smoke ------------------------------------------------------------------------


def misiurewicz_prefix_graph_smoke() -> Bool:
    # The negative control: with its full separator prefix, every exact type
    # within the bound leaves nothing undecided and no obstruction.
    var checked = 0
    var bounded = 0
    for l in range(1, 9):
        for k in range(1, 9):
            if catalogue_denominator(l, k) < 0:
                continue
            var found = extract_catalogue(l, k)
            if not found.accepted():
                bounded += 1
                continue
            if not found.obstruction_free():
                return False
            if found.undecided != 0 or found.cycles() != 0:
                return False
            checked += 1
    if checked != 29 or bounded != 35:
        return False

    # The forward closure of the catalogue of type (1, 3) over the denominator
    # 14, and the exact-type structure it rests on.
    var closure = forward_closure(catalogue(1, 3), 14)
    var expected: List[Int] = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    if len(closure) != len(expected):
        return False
    for i in range(len(expected)):
        if closure[i] != expected[i]:
            return False

    # A single separator leaves a genuine obstruction. The interior cycle is the
    # period-three orbit 3/7 -> 6/7 -> 5/7, that is 6, 12, 10 over 14: three
    # periodic points this prefix never separates and never touches.
    var one_low: List[Int] = [2]
    var one_high: List[Int] = [3]
    var thin = extract(catalogue(1, 3), one_low, one_high, 14)
    if not thin.accepted():
        return False
    if thin.vertices != 12 or thin.undecided != 55 or thin.nonproductive != 17:
        return False
    if thin.merging != 5 or thin.boundary != 0 or thin.interior != 1:
        return False
    if thin.obstruction_free():
        return False

    # The dichotomy is a property of the prefix, not of the cycle. Adding the
    # separator (5, 6) makes 6 an endpoint, and the same cycle becomes a
    # boundary obstruction.
    var interior_lows: List[Int] = [1, 2, 3]
    var interior_highs: List[Int] = [2, 3, 4]
    var interior_case = extract(catalogue(1, 3), interior_lows, interior_highs, 14)
    var boundary_lows: List[Int] = [1, 2, 5]
    var boundary_highs: List[Int] = [2, 3, 6]
    var boundary_case = extract(catalogue(1, 3), boundary_lows, boundary_highs, 14)
    if interior_case.interior != 1 or interior_case.boundary != 0:
        return False
    if boundary_case.boundary != 1 or boundary_case.interior != 0:
        return False
    if interior_case.nonproductive != boundary_case.nonproductive:
        return False

    # A nonproductive set can be entirely transient and merging, with no sink at
    # all. Type (2, 1) over the denominator 4 with no separator has six
    # nonproductive pairs, two of them merging, and no cycle; obstruction_free
    # must still be false, which is why it tests the whole set.
    var no_lows = List[Int]()
    var no_highs = List[Int]()
    var bare = extract(catalogue(2, 1), no_lows, no_highs, 4)
    if not bare.accepted() or bare.nonproductive != 6 or bare.merging != 2:
        return False
    if bare.cycles() != 0 or bare.obstruction_free():
        return False

    # Fail closed, and a refusal is never an empty answer.
    var bad_sep_low: List[Int] = [3]
    var bad_sep_high: List[Int] = [3]
    var mismatched: List[Int] = [1, 2]
    var one: List[Int] = [1]
    if extract(catalogue(1, 3), bad_sep_low, bad_sep_high, 14).accepted():
        return False
    if extract(catalogue(1, 3), mismatched, one, 14).accepted():
        return False
    if extract(one, no_lows, no_highs, 0).accepted():
        return False
    if extract(one, no_lows, no_highs, MAX_PREFIX_GRAPH_DENOMINATOR + 1).accepted():
        return False
    if extract_catalogue(4, 5).accepted():
        return False
    if rejected_extraction().obstruction_free():
        return False

    return (
        not obstruction_free_proves_fibre_triviality() and
        not extractor_decides_persistent_nonseparation() and
        not bounded_refusal_is_evidence_of_no_obstruction()
    )
