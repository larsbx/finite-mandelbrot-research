#!/usr/bin/env python3
"""Python reference for src/C1_separated_density.mojo.

Exact rational arithmetic only. `density(cuts)` is the measure of the pairs of
external angles that a finite set of rational cut angles separates:

    density = 1 - sum_j |I_j|^2 = sum_{i != j} |I_i| |I_j|,

the parameter-space analogue of the common fraction `f_m` of the PSC overlap
route. Usage: separated_density_reference.py
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations

PINNED = {  # cuts -> density; the Mojo smoke target asserts the same instances
    ((1, 3), (2, 3)): Fraction(4, 9),
    ((1, 7), (2, 7), (4, 7)): Fraction(4, 7),
    ((0, 1), (1, 3), (2, 3)): Fraction(2, 3),
    ((1, 3), (2, 3), (1, 3)): Fraction(4, 9),
    ((1, 3),): Fraction(0),
    (): Fraction(0),
}


def normalized(cuts) -> list[Fraction]:
    """Distinct cut angles in [0, 1), ascending; raises on a malformed address."""
    out = set()
    for num, den in cuts:
        if den <= 0 or num < 0 or num >= den:
            raise ValueError(f"cut angle {num}/{den} is not a normalized ray address")
        out.add(Fraction(num, den))
    return sorted(out)


def arcs(cuts) -> list[Fraction]:
    """Lengths of the arcs the distinct cuts induce; one arc of length 1 below two cuts."""
    points = normalized(cuts)
    if len(points) < 2:
        return [Fraction(1)]
    lengths = [b - a for a, b in zip(points, points[1:])]
    lengths.append(1 - points[-1] + points[0])
    return lengths


def density(cuts) -> Fraction:
    lengths = arcs(cuts)
    assert sum(lengths) == 1
    return 1 - sum(x * x for x in lengths)


def pair_sum(cuts) -> Fraction:
    """The same quantity as an explicit sum over ordered pairs of distinct arcs."""
    lengths = arcs(cuts)
    return sum(2 * a * b for a, b in combinations(lengths, 2))


def main() -> int:
    for cuts, expected in PINNED.items():
        assert density(cuts) == expected, cuts
        assert pair_sum(cuts) == expected, cuts
    # Refinement never lowers the density, and only a partition into equal arcs
    # attains the maximum 1 - 1/n for n arcs.
    base = [(k, 12) for k in range(1, 12)]
    for size in range(2, 7):
        for cuts in combinations(base, size):
            here = density(cuts)
            assert 0 <= here <= 1 - Fraction(1, size)
            for extra in base:
                if extra not in cuts:
                    assert density(cuts + (extra,)) >= here, (cuts, extra)
    equal = [(k, 6) for k in range(6)]
    assert density(equal) == 1 - Fraction(1, 6)
    print(f"OK: {len(PINNED)} pinned densities and the refinement bound hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
