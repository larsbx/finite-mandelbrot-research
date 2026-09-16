#!/usr/bin/env python3
"""Python reference for src/C1_separated_density.mojo.

Exact rational arithmetic only. A catalogue prefix is a finite list of two-ray
separators; each assigns every external angle a side, and two angles are
separated exactly when some separator puts them on opposite sides, that is,
when their side signatures differ. The endpoints cut the circle into atoms,
atoms sharing a signature form one undecided class, and

    density = 1 - sum_c |C_c|^2,

the parameter-space analogue of the common fraction `f_m` of the PSC overlap
route. Endpoints must not be flattened into one cut set: with the disjoint
separators (0, 1/4) and (1/2, 3/4) the two outside atoms stay one class, so the
density is 5/8 and not the 3/4 a flat cut set reports.
Usage: separated_density_reference.py
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations

Address = tuple[int, int]
Separator = tuple[Address, Address]

PINNED: dict[tuple[Separator, ...], Fraction] = {  # the Mojo smoke target asserts the same instances
    ((((1, 3)), ((2, 3))),): Fraction(4, 9),
    ((((2, 3)), ((1, 3))),): Fraction(4, 9),
    ((((0, 1)), ((1, 4))), (((1, 2)), ((3, 4)))): Fraction(5, 8),
    ((((1, 7)), ((2, 7))), (((2, 7)), ((4, 7)))): Fraction(4, 7),
    ((((1, 3)), ((2, 3))), (((0, 1)), ((1, 3)))): Fraction(2, 3),
    ((((1, 3)), ((2, 3))), (((1, 3)), ((2, 3)))): Fraction(4, 9),
    (): Fraction(0),
}


def address(pair: Address) -> Fraction:
    num, den = pair
    if den <= 0 or num < 0 or num >= den:
        raise ValueError(f"endpoint {num}/{den} is not a normalized ray address")
    return Fraction(num, den)


def normalized(separators) -> list[tuple[Fraction, Fraction]]:
    """Each separator as `(low, high)`; which side is inside is a convention that
    complements one bit of every signature and leaves the classes alone."""
    out = []
    for left, right in separators:
        a, b = address(left), address(right)
        if a == b:
            raise ValueError("a two-ray separator needs two distinct rays")
        out.append((a, b) if a < b else (b, a))
    return out


def atoms(separators) -> list[tuple[Fraction, tuple[int, ...]]]:
    """`(length, side signature)` for each arc the endpoints cut."""
    pairs = normalized(separators)
    cuts = sorted({x for pair in pairs for x in pair})
    if len(cuts) < 2:
        return [(Fraction(1), ())]
    out = []
    for i, low in enumerate(cuts):
        high = cuts[i + 1] if i + 1 < len(cuts) else cuts[0] + 1
        mid = ((low + high) / 2) % 1
        out.append((high - low, tuple(int(a < mid < b) for a, b in pairs)))
    return out


def classes(separators) -> dict[tuple[int, ...], Fraction]:
    out: dict[tuple[int, ...], Fraction] = {}
    for length, signature in atoms(separators):
        out[signature] = out.get(signature, Fraction(0)) + length
    assert sum(out.values()) == 1
    return out


def density(separators) -> Fraction:
    return 1 - sum(length * length for length in classes(separators).values())


def flattened_density(separators) -> Fraction:
    """The quantity a flat cut set would report; it overstates the decided
    measure whenever two atoms share a signature. Kept only as a negative
    control for the tests."""
    lengths = [length for length, _ in atoms(separators)]
    return 1 - sum(length * length for length in lengths)


def main() -> int:
    for separators, expected in PINNED.items():
        assert density(separators) == expected, separators
    disjoint = PINNED and ((((0, 1)), ((1, 4))), (((1, 2)), ((3, 4))))
    assert density(disjoint) == Fraction(5, 8) and flattened_density(disjoint) == Fraction(3, 4)
    # Refinement never lowers the density, and the classes bound it by 1 - 1/n.
    base = [((k, 12), (j, 12)) for k, j in combinations(range(12), 2)]
    for size in (1, 2, 3):
        for chosen in combinations(base[:9], size):
            here = density(chosen)
            assert 0 <= here <= 1 - Fraction(1, len(classes(chosen)))
            for extra in base[:9]:
                assert density(chosen + (extra,)) >= here, (chosen, extra)
    print(f"OK: {len(PINNED)} pinned densities, the disjoint counterexample, and the refinement bound hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
