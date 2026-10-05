"""Exact-type counts over F_p against exact critical-relation polynomials.

`kernel/mojo/dynamics/critical_type_sieve.mojo` tallies N_p(ell, k) by
iterating the critical orbit. Here the same counts come from root counts of
the exact integer polynomials R_{ell,k} = Q_{ell+k} - Q_ell, inverted over the
order (mu, lambda) <= (ell, k) iff mu <= ell and lambda | k, so the oracle
shares no iteration with the Mojo code.
"""

from __future__ import annotations

import re
import sys
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.python.polynomial.poly_reference import return_poly  # noqa: E402

SRC = ROOT / "kernel/mojo/dynamics/critical_type_sieve.mojo"
GOLDEN = re.compile(r"GoldenCount\((\d+), (\d+), (\d+), (\d+)\)")


def roots_mod_p(ell: int, k: int, p: int) -> int:
    coeffs = [a % p for a in reversed(return_poly(ell, k).coeffs)]
    def value(c: int) -> int:
        acc = 0
        for a in coeffs:
            acc = (acc * c + a) % p
        return acc
    return sum(value(c) == 0 for c in range(p))


@cache
def exact_type_count(p: int, ell: int, k: int) -> int:
    below = [(mu, lam) for mu in range(ell + 1) for lam in range(1, k + 1)
             if k % lam == 0 and (mu, lam) != (ell, k)]
    return roots_mod_p(ell, k, p) - sum(exact_type_count(p, mu, lam) for mu, lam in below)


def golden() -> list[tuple[int, int, int, int]]:
    return [tuple(map(int, row)) for row in GOLDEN.findall(SRC.read_text(encoding="utf-8"))]


def test_every_golden_count_matches_exact_polynomials():
    rows = golden()
    assert len(rows) >= 10
    for p, ell, k, count in rows:
        assert exact_type_count(p, ell, k) == count, (p, ell, k)


def test_the_goldens_cover_gleason_misiurewicz_and_the_empty_preperiod():
    rows = golden()
    assert any(ell == 0 and k >= 3 for _, ell, k, _ in rows)
    assert any(ell >= 2 for _, ell, _, _ in rows)
    assert any(ell == 1 and count == 0 for _, ell, _, count in rows)
