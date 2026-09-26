"""Conformance of the carrier density profile with docs/C1_separated_pair_density.md.

Round-two item R3: a density per level of a carrier's catalogue prefix, the
measure each refinement step decided, and the residue recorded as
non-increasing along the carrier order. The Mojo module is canonical; this
suite asserts the reference model, the constants the Mojo smoke target pins,
and the discipline the module must keep -- above all that a level's separator
is declared, never derived from the level's own address.
"""

from __future__ import annotations

import re
import sys
import tomllib
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.python.c1 import carrier_density_profile_reference as cdp  # noqa: E402
from reference.python.c1 import separated_density_reference as sd  # noqa: E402

DOC = ROOT / "docs" / "C1_separated_pair_density.md"
SRC = ROOT / "src" / "C1_carrier_density_profile.mojo"
DENSITY_SRC = ROOT / "src" / "C1_separated_density.mojo"

BASILICA = ((1, 3), (2, 3))
RABBIT = ((1, 7), (2, 7))
AIRPLANE = ((3, 7), (4, 7))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --- the reference model --------------------------------------------------------


def test_the_reference_agrees_with_itself_on_every_pinned_carrier():
    assert cdp.main() == 0


def test_each_level_reports_the_measure_it_decided():
    rows = cdp.profile((BASILICA, RABBIT))
    assert [row["depth"] for row in rows] == [1, 2]
    assert [row["density"] for row in rows] == [Fraction(4, 9), Fraction(262, 441)]
    assert [row["decided"] for row in rows] == [Fraction(4, 9), Fraction(22, 147)]
    assert [row["residue"] for row in rows] == [Fraction(5, 9), Fraction(179, 441)]
    assert sum(row["decided"] for row in rows) == rows[-1]["density"]


def test_a_prefix_of_a_longer_carrier_is_the_shorter_carrier_s_profile():
    short = cdp.profile((BASILICA, RABBIT))
    long = cdp.profile((BASILICA, RABBIT, AIRPLANE))
    assert long[: len(short)] == short
    assert long[-1]["density"] == Fraction(286, 441) and long[-1]["decided"] == Fraction(8, 147)


def test_the_residue_never_rises_along_a_refinement_order():
    base = [((k, 12), (j, 12)) for k, j in combinations(range(12), 2)][:8]
    for size in (1, 2, 3):
        for chosen in combinations(base, size):
            rows = cdp.profile(chosen)
            assert cdp.residue_non_increasing(rows), chosen
            assert cdp.decided_sums_to_the_density(rows), chosen
            assert all(row["decided"] >= 0 for row in rows), chosen


def test_a_level_decides_nothing_when_its_separator_repeats_an_earlier_one():
    rows = cdp.profile((BASILICA, BASILICA))
    assert rows[1]["decided"] == 0 and rows[1]["residue"] == rows[0]["residue"]


def test_the_profile_is_the_prefix_density_and_nothing_new():
    for depth, row in enumerate(cdp.profile((BASILICA, RABBIT, AIRPLANE)), start=1):
        assert row["density"] == sd.density((BASILICA, RABBIT, AIRPLANE)[:depth])


# --- what the module may not do -------------------------------------------------


def test_the_separator_of_a_level_is_declared_not_derived():
    """The correction to N3: a separator needs a declared co-landing pair, so
    the module takes one per level and never builds one from the address."""
    src = text(SRC)
    start = src.index("def carrier_density_profile(")
    signature = src[start:src.index(") -> CarrierDensityProfile:", start)]
    for argument in ("level_nums", "level_dens", "lefts_n", "lefts_d", "rights_n", "rights_d",
                     "tags", "co_landings"):
        assert argument in signature
    assert "separator declared for each level is a separate input" in src
    assert "vacuous construction" in src
    assert "docs/C1_admissible_separator_codes.md" in src


def test_the_declared_separator_must_also_be_admissible():
    """Declaring a pair is not enough: two arbitrary rational angles are a cut,
    and measuring one would report an unproved separation as a decided one."""
    src = text(SRC)
    gate = src[src.index("def admissible_separator("):src.index("def _prefix(")]
    assert "if not co_landing:" in gate
    for tag in ("LANDING_RATIONAL_RAY", "LANDING_PARABOLIC", "LANDING_HYPERBOLIC_BOUNDARY"):
        assert tag in gate
    assert "return ln * rd != rn * ld" in gate
    body = src[src.index("def carrier_density_profile("):src.index("# --- non-claims")]
    assert "if not admissible_separator(" in body


def test_the_admissibility_gate_is_the_same_on_both_sides():
    """The oracle applies the gate the Mojo module applies, on the same codes."""
    assert (cdp.RATIONAL_RAY, cdp.PARABOLIC, cdp.HYPERBOLIC_BOUNDARY) == (1, 2, 3)
    for name, code in (("LANDING_RATIONAL_RAY", 1), ("LANDING_PARABOLIC", 2),
                       ("LANDING_HYPERBOLIC_BOUNDARY", 3)):
        assert f"comptime {name}: Int64 = {code}" in text(SRC)
    basilica = ((1, 3), (2, 3))
    assert cdp.admissible(basilica, cdp.RATIONAL_RAY, True)
    assert not cdp.admissible(basilica, 0, True)          # the generic-boundary tag has no code
    assert not cdp.admissible(basilica, cdp.RATIONAL_RAY, False)
    assert not cdp.admissible(((1, 3), (1, 3)), cdp.RATIONAL_RAY, True)
    with pytest.raises(ValueError, match="inadmissible separator"):
        cdp.profile((basilica,), cdp.RATIONAL_RAY, False)


def test_the_mojo_smoke_exercises_the_gate_in_both_directions():
    """A gate that refused everything would pass every rejection case above."""
    src = text(SRC)
    assert "var generic: List[Int64] = [0]" in src and "var mlc: List[Int64] = [4]" in src
    assert "var undeclared: List[Bool] = [False]" in src
    assert "_is(admitted.levels[0].density, 4, 9)" in src


def test_non_claims_return_false_in_mojo():
    src = text(SRC)
    for name in ("profile_decides_carrier_membership", "residue_zero_at_some_level_is_reachable",
                 "density_increment_measures_carrier_progress"):
        block = src[src.index(f"def {name}() -> Bool:"):]
        assert "return False" in block.split("\n\n")[0]


def test_exact_arithmetic_only():
    src = text(SRC)
    assert "from finite_exact.rat_q import Q" in src
    assert not re.search(r"\bFloat(?:16|32|64|Literal)?\b", src)
    assert not re.search(r"(?<![\w.])\d+\.\d", src)
    assert "docs/rational-interval-arithmetic-spec.md" in src


def test_the_module_fails_closed_rather_than_returning_an_empty_profile():
    src = text(SRC)
    assert src.count("return rejected_profile()") >= 8
    assert "def rejected_profile()" in src
    body = src[src.index("def carrier_density_profile("):src.index("# --- non-claims")]
    for guard in ("if not here.accepted():", "decided.lt(Q.zero())", "previous_residue.lt(here.residue)",
                  "not total_decided.eq(previous_density)"):
        assert guard in body


def test_the_kernel_is_the_one_the_density_note_governs():
    assert "from C1_separated_density import" in text(SRC)
    assert "separated_pair_density" in text(SRC) and "def separated_pair_density(" in text(DENSITY_SRC)


# --- governance -----------------------------------------------------------------


def test_the_regime_correspondence_binds_the_profile_symbol():
    spec = tomllib.loads(text(ROOT / "spec" / "regime_correspondences.toml"))
    entry = next(c for c in spec["correspondence"] if c["id"] == "separated-pair-density")
    assert "src/C1_carrier_density_profile.mojo::carrier_density_profile" in entry["symbols"]
    assert "any verdict on the carrier whose levels order the prefix" in entry["does_not_inherit"]
    assert text(SRC).count("# Regime correspondence: separated-pair-density") == 1


def test_the_note_records_the_step_as_taken():
    body = text(DOC)
    assert "src/C1_carrier_density_profile.mojo" in body
    assert "Next step" in body


def test_mojo_smoke_pins_the_same_constants():
    src = text(SRC)
    for fragment in ("_is(basilica.levels[0].density, 4, 9)", "_is(refined.levels[1].density, 262, 441)",
                     "_is(refined.levels[1].decided, 22, 147)", "_is(deeper.levels[2].decided, 8, 147)",
                     "refined.residue_non_increasing"):
        assert fragment in src
    assert "carrier_density_profile_smoke" in text(ROOT / "src" / "smoke_tests.mojo")
