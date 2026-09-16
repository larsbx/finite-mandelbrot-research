#!/usr/bin/env python3
"""Python reference for src/C1_misiurewicz_prefix_graph.mojo.

Integer arithmetic only, everything inside `Z/den`.

The obstruction extractor of `docs/p1-overlap-minimal-obstruction-2026-09-14.md`
in `larsbx/pisot-substitution-conjecture-research`, run on the finite graphs the
exact-type catalogue supplies. The pipeline is the one route F1 describes
abstractly in `docs/C1_F1_obstruction_extraction.md`:

    vertices   forward orbit closure of a catalogue under doubling
    pairs      the unordered non-diagonal pairs of vertices
    N          the pairs the separator prefix does not separate
    invariant  the largest forward-invariant subset of N
    sinks      the cycles of the invariant set, its sink components
    dichotomy  each cycle is a boundary or an interior obstruction

Doubling is a function, so the pair graph has out-degree at most one and each
component falls into exactly one cycle: the sink components are the cycles, and
no strongly-connected-component search is needed.

`main` replays the negative control: on every exact type within the bound, the
full separator prefix leaves no obstruction at all.
Usage: misiurewicz_prefix_graph_reference.py
"""

from __future__ import annotations

import sys

import misiurewicz_catalogue_reference as mc

# One bound governs the graph: the denominator. Vertices live in `Z/den`, so it
# caps the vertex count, and the pair count is at most den (den - 1) / 2. The
# Mojo module carries the same constant, so the two agree on every refusal.
MAX_PREFIX_GRAPH_DENOMINATOR = 256
REGRESSION = 8


# --- the finite objects ---------------------------------------------------------


def forward_closure(seed: list[int], den: int) -> list[int] | None:
    """The forward orbit closure of `seed` under doubling in `Z/den`, ascending,
    or None when it would exceed the vertex bound or the seed is out of range."""
    if den <= 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR or any(x < 0 or x >= den for x in seed):
        return None
    seen, stack = set(seed), list(seed)
    while stack:
        point = (2 * stack.pop()) % den
        if point not in seen:
            seen.add(point)
            stack.append(point)
    return sorted(seen)


def side(point: int, separator: tuple[int, int], den: int) -> int:
    """Which side of a two-ray separator a point falls on: `1` on the arc running
    counterclockwise from the first ray to the second, `0` on the complement.
    Exchanging the two rays names the complementary side."""
    low, high = separator
    return 1 if ((point - low) % den) < ((high - low) % den) else 0


def signature(point: int, separators: list[tuple[int, int]], den: int) -> tuple[int, ...]:
    return tuple(side(point, s, den) for s in separators)


def separated(a: int, b: int, separators: list[tuple[int, int]], den: int) -> bool:
    """Two points are separated by the prefix exactly when some separator puts
    them on opposite sides, that is when their side signatures differ."""
    return signature(a, separators, den) != signature(b, separators, den)


def successor(pair: tuple[int, int], den: int) -> tuple[int, int] | None:
    """The image of an unordered pair under doubling, or None when the two
    points share an image. A collapsing pair leaves the graph: it has no
    successor, so it cannot witness persistent non-separation here, and the
    finite fact that decides it is `b - a == den / 2`."""
    a, b = (2 * pair[0]) % den, (2 * pair[1]) % den
    return None if a == b else (min(a, b), max(a, b))


def undecided_pairs(vertices: list[int], separators: list[tuple[int, int]], den: int) -> list[tuple[int, int]]:
    """The pairs the prefix does not separate *at this step*. These are the pairs
    sharing a side signature, so grouping by signature costs the size of the
    answer rather than the square of the vertex count.

    This is one step, not the verdict: an undecided pair whose successor is
    separated is still productive. The verdict is `nonproductive`."""
    classes: dict[tuple[int, ...], list[int]] = {}
    for point in vertices:
        classes.setdefault(signature(point, separators, den), []).append(point)
    return sorted((a, b) for c in classes.values()
                  for i, a in enumerate(c) for b in c[i + 1:])


def nonproductive(vertices: list[int], separators: list[tuple[int, int]], den: int) -> set[tuple[int, int]]:
    """The pairs no iterate of doubling ever separates.

    A pair is productive when it is separated now, or when its successor is
    productive; the fixpoint below is that definition read backwards from the
    separated pairs, which is how `nonproductive_overlap_states` works on the
    overlap graph. Forward closedness is then a lemma rather than a computation:
    a nonproductive pair cannot have a productive successor, since a separation
    reached from the successor is reached from the pair one step earlier.

    A merging pair, whose two points share an image, has no successor and is
    never separated, so it is nonproductive. Treating it as productive would be
    the substantive error: those two addresses are exactly the ones the dynamics
    can never tell apart, so they are an obstruction, not a discharge."""
    pairs = [(a, b) for i, a in enumerate(vertices) for b in vertices[i + 1:]]
    # One signature per point rather than one separator sweep per pair.
    marks = {x: signature(x, separators, den) for x in vertices}
    productive = {p for p in pairs if marks[p[0]] != marks[p[1]]}
    while True:
        grown = {p for p in pairs
                 if p not in productive and (s := successor(p, den)) is not None and s in productive}
        if not grown:
            return {p for p in pairs if p not in productive}
        productive |= grown


def sink_cycles(invariant: set[tuple[int, int]], den: int) -> list[tuple[tuple[int, int], ...]]:
    """The sink components of the nonproductive set. Doubling is a function, so
    the pair graph has out-degree at most one and each component falls into
    exactly one cycle; the cycles are therefore the sink components and no
    strongly-connected-component search is needed. A merging pair has no
    successor, so it is a transient nonproductive pair, never a sink.

    Each cycle is rotated to start at its least pair and the list is sorted, so
    the answer does not depend on traversal order."""
    seen: set[tuple[int, int]] = set()
    found: list[tuple[tuple[int, int], ...]] = []
    for start in sorted(invariant):
        if start in seen:
            continue
        order: dict[tuple[int, int], int] = {}
        walk, point = [], start
        while point in invariant and point not in order:
            order[point] = len(walk)
            walk.append(point)
            point = successor(point, den)
        if point in order:
            cycle = walk[order[point]:]
            if not set(cycle) & seen:
                least = cycle.index(min(cycle))
                found.append(tuple(cycle[least:] + cycle[:least]))
        seen |= set(walk)
    return sorted(found)


def endpoints(separators: list[tuple[int, int]]) -> set[int]:
    return {e for s in separators for e in s}


def is_boundary(cycle: tuple[tuple[int, int], ...], separators: list[tuple[int, int]]) -> bool:
    """The dichotomy. A cycle is a boundary obstruction when some point on it is
    a separator endpoint: the object may lie on the separation line itself, which
    is the `BoundaryEqualityCandidate` of the carrier vocabulary and the aligned
    obstruction of the overlap route. Otherwise it is an interior obstruction,
    no separator boundary is ever hit, which is `CarrierTooCoarse`: the prefix is
    not fine enough, and the strict-zipper case of the overlap route."""
    ends = endpoints(separators)
    return any(a in ends or b in ends for (a, b) in cycle)


# --- the extractor --------------------------------------------------------------


class Extraction:
    """A rejected extraction carries no counts. `rejected` is sticky: a bounded
    search that failed is not evidence that no obstruction exists."""

    __slots__ = ("vertices", "undecided", "nonproductive", "merging",
                 "boundary", "interior", "cycles", "rejected")

    def __init__(self, vertices=0, undecided=0, nonproductive=0, merging=0,
                 boundary=(), interior=(), rejected=False):
        self.vertices = vertices
        self.undecided = undecided
        self.nonproductive = nonproductive
        self.merging = merging
        self.boundary = tuple(boundary)
        self.interior = tuple(interior)
        self.cycles = tuple(sorted(self.boundary + self.interior))
        self.rejected = rejected

    @property
    def accepted(self) -> bool:
        return not self.rejected

    @property
    def obstruction_free(self) -> bool:
        """No pair survives: nothing the prefix leaves undecided stays undecided
        under doubling. Only an accepted extraction can be obstruction free, so a
        bounded search that failed never reads as a clean verdict. The test is
        the whole nonproductive set, not just its sinks, because a merging pair
        is nonproductive without lying on any cycle."""
        return self.accepted and self.nonproductive == 0

    def __repr__(self) -> str:
        if self.rejected:
            return "Extraction(rejected)"
        return (f"Extraction(vertices={self.vertices}, undecided={self.undecided}, "
                f"nonproductive={self.nonproductive}, merging={self.merging}, "
                f"boundary={len(self.boundary)}, interior={len(self.interior)})")


def rejected_extraction() -> Extraction:
    return Extraction(rejected=True)


def extract(seed: list[int], separators: list[tuple[int, int]], den: int) -> Extraction:
    """Run the pipeline on the forward closure of `seed` in `Z/den`. Fails closed
    on a malformed separator, an out-of-range point, and either bound."""
    if den <= 0 or den > MAX_PREFIX_GRAPH_DENOMINATOR or not seed:
        return rejected_extraction()
    for low, high in separators:
        if low < 0 or high < 0 or low >= den or high >= den or low == high:
            return rejected_extraction()
    vertices = forward_closure(seed, den)
    if vertices is None:
        return rejected_extraction()
    undecided = undecided_pairs(vertices, separators, den)
    bad = nonproductive(vertices, separators, den)
    cycles = sink_cycles(bad, den)
    boundary = [c for c in cycles if is_boundary(c, separators)]
    interior = [c for c in cycles if not is_boundary(c, separators)]
    return Extraction(
        vertices=len(vertices),
        undecided=len(undecided),
        nonproductive=len(bad),
        merging=sum(1 for p in bad if successor(p, den) is None),
        boundary=boundary,
        interior=interior,
    )


def catalogue_separators(preperiod: int, period: int) -> list[tuple[int, int]] | None:
    """The full separator prefix of an exact type: consecutive points of the
    forward closure, which is the finest prefix this catalogue supplies."""
    den = mc.catalogue_denominator(preperiod, period)
    if den < 0:
        return None
    vertices = forward_closure(mc.catalogue(preperiod, period), den)
    if vertices is None or len(vertices) < 2:
        return []
    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]


def extract_catalogue(preperiod: int, period: int, separators=None) -> Extraction:
    """The extractor on an exact type, with its full separator prefix by default."""
    den = mc.catalogue_denominator(preperiod, period)
    if den < 0:
        return rejected_extraction()
    if separators is None:
        separators = catalogue_separators(preperiod, period)
    return extract(mc.catalogue(preperiod, period), separators, den)


# --- non-claims -----------------------------------------------------------------


def obstruction_free_proves_fibre_triviality() -> bool:
    """An empty obstruction set is a fact about one finite prefix graph. Fibre
    triviality for this class is the imported tag `KnownTrivialFiberClass`."""
    return False


def extractor_decides_persistent_nonseparation() -> bool:
    """Persistent non-separation quantifies over every prefix. This runs one."""
    return False


# --- the regression -------------------------------------------------------------


def main() -> int:
    """The negative control: with its full separator prefix, every exact type
    within the bound is obstruction free, and every rejection is sticky."""
    checked, bounded = 0, 0
    for preperiod in range(1, REGRESSION + 1):
        for period in range(1, REGRESSION + 1):
            if mc.catalogue_denominator(preperiod, period) < 0:
                continue
            found = extract_catalogue(preperiod, period)
            if not found.accepted:
                # Past a bound is a refusal, not a pass. Counted, never skipped
                # silently, and it says nothing about that type either way.
                bounded += 1
                continue
            if not found.obstruction_free:
                print(f"FAIL: ({preperiod}, {period}) has obstructions: {found}")
                return 1
            if found.undecided != 0:
                print(f"FAIL: ({preperiod}, {period}) full prefix left {found.undecided} undecided")
                return 1
            checked += 1
    for bad in (rejected_extraction(),):
        if bad.accepted or bad.obstruction_free:
            print("FAIL: a rejected extraction must not read as obstruction free")
            return 1
    print(f"OK: the full separator prefix leaves no obstruction on {checked} exact types "
          f"({bounded} more are past a bound and were refused, not passed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
