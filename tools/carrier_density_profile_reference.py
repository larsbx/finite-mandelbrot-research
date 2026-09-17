#!/usr/bin/env python3
"""Python reference for src/C1_carrier_density_profile.mojo.

Round-two item R3, the step `docs/C1_separated_pair_density.md` left open:
attach a density to each level of a carrier's catalogue prefix, so a refinement
step reports the measure it decided as well as the addresses it added, and
record whether the residue is non-increasing along the carrier-refinement
order.

A carrier level does not supply a separator. `docs/C1_admissible_separator_codes.md`
requires a separator to carry accepted landing tags on both rays and a declared
co-landing pair, which an address alone cannot supply, so the separator
declared for each level is a separate input here exactly as it is in the Mojo
module. The classical wake pairs this file pins -- 1/3 with 2/3, 1/7 with 2/7,
3/7 with 4/7, 2/5 with 3/5 -- are declared imports from Douady-Hubbard wake
theory, not quantities derived from the carrier's own addresses.

The requirement is enforced rather than assumed, on both sides. `admissible`
below is the Mojo module's `admissible_separator`: an accepted landing tag, a
declared co-landing pair, positive denominators and two distinct rays. Two
arbitrary rational angles are a cut, not a separator, and measuring one would
report an unproved separation as a decided one.

Two facts are checked rather than assumed: the residue is non-increasing along
the prefix, because adding a separator refines the signature partition and a
refinement never raises a sum of squares; and the decided increments sum to the
final density. Both are exact over unbounded rationals.

Usage: carrier_density_profile_reference.py
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations

from separated_density_reference import Separator, classes, density

Address = tuple[int, int]

# The landing tags of docs/C1_admissible_separator_codes.md, as the integer
# codes src/C1_carrier_density_profile.mojo uses. Everything else -- the
# generic-boundary landing and the MLC binding the spec forbids included --
# is inadmissible by having no code at all.
RATIONAL_RAY, PARABOLIC, HYPERBOLIC_BOUNDARY = 1, 2, 3
ACCEPTED_TAGS = frozenset({RATIONAL_RAY, PARABOLIC, HYPERBOLIC_BOUNDARY})


def admissible(separator: Separator, tag: int, co_landing: bool) -> bool:
    """The gate `admissible_separator` applies in the Mojo module."""
    (ln, ld), (rn, rd) = separator
    return bool(co_landing) and tag in ACCEPTED_TAGS and ld > 0 and rd > 0 and ln * rd != rn * ld


# A carrier prefix, and the separator declared for each of its levels: the two
# rays that co-land at the root of that level's hyperbolic component.
PINNED: dict[str, tuple[tuple[Address, ...], tuple[Separator, ...]]] = {
    "basilica then rabbit": (((1, 3), (1, 7)), ((((1, 3)), ((2, 3))), (((1, 7)), ((2, 7))))),
    "rabbit then airplane": (((1, 7), (3, 7)), ((((1, 7)), ((2, 7))), (((3, 7)), ((4, 7))))),
    "basilica alone": (((1, 3),), ((((1, 3)), ((2, 3))),)),
    "basilica, rabbit, airplane": (
        ((1, 3), (1, 7), (3, 7)),
        ((((1, 3)), ((2, 3))), (((1, 7)), ((2, 7))), (((3, 7)), ((4, 7)))),
    ),
}


def profile(separators: tuple[Separator, ...], tag: int = RATIONAL_RAY, co_landing: bool = True) -> list[dict[str, object]]:
    """One row per level: the density and residue of the prefix up to it, the
    measure that level decided, and the number of signature classes. Every
    separator must be admissible; an inadmissible one is refused rather than
    measured, exactly as the Mojo module rejects the whole profile."""
    if not all(admissible(s, tag, co_landing) for s in separators):
        raise ValueError("inadmissible separator: no accepted landing tag, or no declared co-landing")
    rows: list[dict[str, object]] = []
    previous = Fraction(0)
    for depth in range(1, len(separators) + 1):
        prefix = separators[:depth]
        here = density(prefix)
        rows.append({"depth": depth, "density": here, "residue": 1 - here,
                     "decided": here - previous, "classes": len(classes(prefix))})
        previous = here
    return rows


def residue_non_increasing(rows) -> bool:
    return all(b["residue"] <= a["residue"] for a, b in zip(rows, rows[1:]))


def decided_sums_to_the_density(rows) -> bool:
    return not rows or sum(row["decided"] for row in rows) == rows[-1]["density"]


def main() -> int:
    for name, (_, separators) in PINNED.items():
        rows = profile(separators)
        assert len(rows) == len(separators), name
        assert residue_non_increasing(rows), name
        assert decided_sums_to_the_density(rows), name
        assert all(row["decided"] >= 0 for row in rows), name
        print(f"{name}: " + ", ".join(f"level {r['depth']} density {r['density']} decided {r['decided']}" for r in rows))
    # The two facts hold for every prefix of every small catalogue, not only the pinned ones.
    base: list[Separator] = [((k, 12), (j, 12)) for k, j in combinations(range(12), 2)][:9]
    for size in (1, 2, 3):
        for chosen in combinations(base, size):
            rows = profile(chosen)
            assert residue_non_increasing(rows) and decided_sums_to_the_density(rows), chosen
    # The gate refuses, and is not a gate that refuses nothing: the basilica
    # pair above is accepted, and the same pair fails on each missing licence.
    basilica: Separator = ((1, 3), (2, 3))
    assert admissible(basilica, RATIONAL_RAY, True)
    assert admissible(basilica, PARABOLIC, True) and admissible(basilica, HYPERBOLIC_BOUNDARY, True)
    for tag, co_landing in ((0, True), (4, True), (RATIONAL_RAY, False)):
        try:
            profile((basilica,), tag, co_landing)
        except ValueError:
            continue
        raise AssertionError(f"inadmissible separator measured: tag {tag}, co-landing {co_landing}")
    assert not admissible(((1, 3), (1, 3)), RATIONAL_RAY, True), "a cut needs two distinct rays"
    print(f"OK: {len(PINNED)} pinned carrier profiles; residue non-increasing and increments exact on every prefix.")
    print("OK: inadmissible separators (forbidden tag, undeclared co-landing, coincident rays) are refused.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
