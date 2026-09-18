"""The corpora this repository's oracles draw from, declared and checked.

Round-three item R9: `larsbx/meta_test` requires a generator to declare a
codomain refinement, and the facility is vendored from
`larsbx/finite-math-kernels` (`tools/oracle_refinement`, specified in its
`docs/generator-refinement-spec.md`).

Every test here is a negative control as well as a check: each one names the
corpus that would have passed while saying nothing.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import carrier_density_profile_reference as cdp  # noqa: E402
import exact_arithmetic_property_oracle as probe  # noqa: E402
from oracle_refinement import audit_all  # noqa: E402


# --- the exact-arithmetic property probe -------------------------------------------


def test_the_probe_corpus_meets_its_declaration():
    assert probe.distribution_problems() == ()


def test_the_probe_is_judged_on_every_call_not_only_the_printed_operands():
    """A fraction draws two integers and an interval draws two fractions."""
    draws = probe.drawn()
    assert len(draws.integers) == 2 * probe.Z_CASES + 2 * len(draws.fractions)
    assert len(draws.fractions) == 2 * probe.Q_CASES + 2 * len(draws.intervals)
    assert len(draws.intervals) == 2 * probe.I_CASES


def test_the_probe_stream_still_misses_zero_the_unit_and_the_point_interval():
    """The declared gaps, pinned. Closing one must be deliberate: this fails
    first, and then the declaration is revised rather than quietly kept."""
    draws = probe.drawn()
    assert not any(v == 0 for v in draws.integers)
    assert not any(abs(v) == 1 for v in draws.integers)
    assert not any(f == 0 or f.denominator == 1 for f in draws.fractions)
    assert not any(lo == hi for lo, hi in draws.intervals)
    assert any(abs(v) >= 1 << 63 for v in draws.integers)


def test_every_declared_gap_names_what_it_leaves_unexercised():
    for refinement in probe.REFINEMENTS:
        for cls in refinement.classes:
            if not cls.required:
                assert len(cls.reason) > 40, (refinement.name, cls.name)


# --- the carrier-density sweep ------------------------------------------------------


def test_the_sweep_corpus_meets_its_declaration():
    assert cdp.sweep_problems() == ()


def test_the_sweep_reaches_more_than_one_left_endpoint_and_both_arc_extremes():
    base = cdp.sweep()
    assert len({cdp._numerators(s)[0] for s in base}) > 1
    widths = {cdp._gap(s) for s in base}
    assert 1 in widths and cdp.TWELFTH // 2 in widths


def test_the_corpus_the_sweep_used_to_draw_is_refused_by_name():
    """The historical control. `combinations(range(12), 2)[:9]` is nine
    separators that all start at `0/12`: a pencil of rays through one point,
    swept as though it were a catalogue, with no crossing or nested pair in it."""
    pencil = [((k, 12), (j, 12)) for k, j in combinations(range(12), 2)][:9]
    problems = audit_all(((cdp.SWEEP, pencil), (cdp.SWEEP_PAIR, list(combinations(pencil, 2)))))
    assert len(problems) == 3
    assert "a left endpoint other than 0" in problems[0]
    assert "'crossing'" in problems[1] and "'nested'" in problems[2]


def test_the_sweep_pairs_reach_every_relative_position():
    pairs = list(combinations(cdp.sweep(), 2))
    assert any(cdp._crosses(a, b) for a, b in pairs)
    assert any(cdp._nests(a, b) for a, b in pairs)
    assert any(not cdp._crosses(a, b) and not cdp._nests(a, b) for a, b in pairs)


def test_the_sweep_declares_the_denominator_it_does_not_leave():
    """The gap is stated rather than implied: one denominator wide, with the
    classical wakes covered by the pinned profiles instead."""
    missed = [c for c in cdp.SWEEP.classes if not c.required]
    assert [c.name for c in missed] == ["endpoints off the twelfths"]
    assert "PINNED" in missed[0].reason or "pinned" in missed[0].reason
