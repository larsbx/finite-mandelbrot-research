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


def profile(separators: tuple[Separator, ...]) -> list[dict[str, object]]:
    """One row per level: the density and residue of the prefix up to it, the
    measure that level decided, and the number of signature classes."""
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
    print(f"OK: {len(PINNED)} pinned carrier profiles; residue non-increasing and increments exact on every prefix.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
