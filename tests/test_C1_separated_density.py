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

SEP_13_23 = ((((1, 3)), ((2, 3))),)
DISJOINT = ((((0, 1)), ((1, 4))), (((1, 2)), ((3, 4))))


def test_pinned_densities():
    assert sd.main() == 0
    assert sd.density(SEP_13_23) == Fraction(4, 9)
    assert sd.density(((((1, 7)), ((2, 7))), (((2, 7)), ((4, 7))))) == Fraction(4, 7)


def test_disjoint_separators_keep_their_outside_atoms_in_one_class():
    # The finding of the review on PR #3: flattening endpoints into one cut set
    # counts the two outside atoms as distinct and overstates the measure.
    assert sd.density(DISJOINT) == Fraction(5, 8)
    assert sd.flattened_density(DISJOINT) == Fraction(3, 4)
    assert len(sd.classes(DISJOINT)) == 3 and len(sd.atoms(DISJOINT)) == 4
    assert sorted(sd.classes(DISJOINT).values()) == [Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)]


def test_which_side_is_inside_is_a_convention():
    for separators in (SEP_13_23, DISJOINT):
        flipped = tuple((right, left) for left, right in separators)
        assert sd.density(flipped) == sd.density(separators)
        assert sorted(sd.classes(flipped).values()) == sorted(sd.classes(separators).values())


def test_no_separator_decides_nothing_and_repetition_is_not_refinement():
    assert sd.density(()) == 0 and sd.atoms(()) == [(Fraction(1), ())]
    assert sd.density(SEP_13_23 + SEP_13_23) == sd.density(SEP_13_23)


def test_malformed_separators_are_refused():
    for separators in (((((1, 0)), ((1, 3))),), ((((7, 5)), ((1, 3))),), ((((-1, 3)), ((1, 3))),),
                       ((((1, 3)), ((1, 3))),), ((((1, 3)), ((2, 6))),)):
        with pytest.raises(ValueError):
            sd.density(separators)


def test_classes_bound_the_density_and_refinement_never_lowers_it():
    base = [((k, 8), (j, 8)) for k, j in combinations(range(8), 2)]
    for size in (1, 2, 3):
        for chosen in combinations(base[:7], size):
            here = sd.density(chosen)
            assert here == 1 - sum(x * x for x in sd.classes(chosen).values())
            assert 0 <= here <= 1 - Fraction(1, len(sd.classes(chosen)))
            for extra in base[:7]:
                assert sd.density(chosen + (extra,)) >= here


def test_mojo_smoke_pins_the_same_instances():
    src = text(SRC)
    for fragment in ('_is(single, 4, 9)', '_is(disjoint, 5, 8)', '_is(nested, 4, 7)', '_is(refined, 2, 3)',
                     'disjoint.atoms == 4 and disjoint.classes == 3', 'disjoint.density.lt(Q(3, 4))'):
        assert fragment in src
    assert "separated_density_smoke" in text(ROOT / "src" / "smoke_tests.mojo")
