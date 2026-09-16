"""Conformance of the separated-pair density with docs/C1_separated_pair_density.md."""

from __future__ import annotations

import re
import sys
import tomllib
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import separated_density_reference as sd  # noqa: E402

DOC = ROOT / "docs" / "C1_separated_pair_density.md"
SRC = ROOT / "src" / "C1_separated_density.mojo"
LEDGER_DOC = ROOT / "docs" / "C1_theorem_tag_import_ledger.md"
LEDGER_SRC = ROOT / "src" / "C1_theorem_tag_import_ledger.mojo"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --- documentation and governance ----------------------------------------------


def test_density_term_is_declared_with_genealogy_and_leaks():
    body = text(DOC)
    assert body.splitlines()[2].startswith("Status:")
    assert "Terminology declaration: separated-pair density" in body
    for field in ("Genealogy:", "Bridge claim:", "Known leaks:", "Use discipline:"):
        assert field in body
    assert "definition-only" in body
    assert "separated-pair density" in text(ROOT / "docs" / "terminology-registry.md")


def test_non_claims_return_false_in_mojo():
    src = text(SRC)
    for name in ("density_one_implies_every_pair_separated", "finite_prefix_density_decides_persistent_non_separation",
                 "density_is_harmonic_measure_of_the_boundary"):
        block = src[src.index(f"def {name}() -> Bool:"):]
        assert "return False" in block.split("\n\n")[0]
    # Exact arithmetic only: the unbounded rational type, no float type or literal.
    assert "from finite_exact.rat_q import Q" in src
    assert not re.search(r"\bFloat(?:16|32|64|Literal)?\b", src)
    assert not re.search(r"(?<![\w.])\d+\.\d", src)
    assert "docs/rational-interval-arithmetic-spec.md" in src


def test_harmonic_measure_tag_is_class_specific_scaffolded_and_cannot_discharge_a_pair():
    src = text(LEDGER_SRC)
    block = src[src.index("def harmonic_measure_fibre_triviality_tag_ready"):src.index("def generic_mlc_import_admissible")]
    assert "ImportConclusionKind.harmonic_measure_fibre_triviality()" in block
    assert "ImportStrengthClass.classical_class_specific()" in block and "ImportStatus.scaffolded()" in block
    assert "def harmonic_measure_tag_discharges_a_named_pair() -> Bool:" in src
    assert "return False" in block[block.index("def harmonic_measure_tag_discharges_a_named_pair"):]
    doc = text(LEDGER_DOC)
    section = doc[doc.index("### Harmonic-measure-almost-every fibre triviality"):doc.index("## Forbidden imports")]
    for field in ("theorem_source", "measure_declared", "exceptional_set_is_null_not_empty",
                  "parameter_not_selected_from_the_exceptional_set", "adapter_domain_matches", "conclusion_scope"):
        assert field in section
    assert "may not discharge" in section and "not a residual exit" in section
    assert "Graczyk" in section and "Smirnov" in section


def test_regime_correspondence_binds_the_density_symbol():
    spec = tomllib.loads(text(ROOT / "spec" / "regime_correspondences.toml"))
    entry = next(c for c in spec["correspondence"] if c["id"] == "separated-pair-density")
    assert "harmonic measure on the boundary" in entry["does_not_inherit"]
    assert "separation of a named pair" in entry["does_not_inherit"]
    for symbol in entry["symbols"]:
        path, name = symbol.split("::")
        assert path == "src/C1_separated_density.mojo" and f"def {name}(" in text(SRC)
    assert text(SRC).count("# Regime correspondence: separated-pair-density") == len(entry["symbols"])


# --- the reference model --------------------------------------------------------


def test_pinned_densities():
    assert sd.main() == 0
    assert sd.density(((1, 3), (2, 3))) == Fraction(4, 9)
    assert sd.density(((1, 7), (2, 7), (4, 7))) == Fraction(4, 7)
    assert sd.arcs(((1, 7), (2, 7), (4, 7))) == [Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]


def test_fewer_than_two_distinct_cuts_decide_nothing():
    for cuts in ((), ((1, 3),), ((1, 3), (2, 6))):
        assert sd.density(cuts) == 0 and sd.arcs(cuts) == [Fraction(1)]


def test_malformed_addresses_are_refused():
    for cuts in (((1, 0),), ((7, 5),), ((-1, 3),), ((3, 3),)):
        with pytest.raises(ValueError):
            sd.density(cuts)


def test_density_equals_the_ordered_pair_sum_and_respects_the_arc_bound():
    base = [(k, 10) for k in range(10)]
    for size in range(2, 6):
        for cuts in combinations(base, size):
            here = sd.density(cuts)
            assert here == sd.pair_sum(cuts)
            assert 0 <= here <= 1 - Fraction(1, size)


def test_refinement_never_lowers_the_density():
    base = [(k, 9) for k in range(9)]
    for size in range(1, 5):
        for cuts in combinations(base, size):
            for extra in base:
                if extra not in cuts:
                    assert sd.density(cuts + (extra,)) >= sd.density(cuts)


def test_equal_arcs_attain_the_maximum():
    for n in range(2, 13):
        assert sd.density(tuple((k, n) for k in range(n))) == 1 - Fraction(1, n)


def test_mojo_smoke_pins_the_same_instances():
    src = text(SRC)
    for fragment in ('var thirds_d: List[Int64] = [3, 3]', 'var rabbit_d: List[Int64] = [7, 7, 7]',
                     '_is(thirds, 4, 9)', '_is(rabbit, 4, 7)', '_is(refined, 2, 3)', '_is(repeated, 4, 9)'):
        assert fragment in src
    assert "separated_density_smoke" in text(ROOT / "src" / "smoke_tests.mojo")
