"""Conformance of the exact-type catalogue with docs/C1_misiurewicz_catalogue.md."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import misiurewicz_catalogue_reference as mc  # noqa: E402

DOC = ROOT / "docs" / "C1_misiurewicz_catalogue.md"
SRC = ROOT / "src" / "misiurewicz_catalogue.mojo"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --- documentation and governance ----------------------------------------------


def test_catalogue_term_is_declared_with_genealogy_and_leaks():
    body = text(DOC)
    assert body.splitlines()[2].startswith("Status:")
    assert "Terminology declaration: exact-type catalogue" in body
    for field in ("Genealogy:", "Bridge claim:", "Known leaks:", "Use discipline:"):
        assert field in body
    assert "definition-only" in body
    assert "exact-type catalogue" in text(ROOT / "docs" / "terminology-registry.md")


def test_non_claims_return_false_in_mojo():
    src = text(SRC)
    for name in ("catalogue_is_a_set_of_parameters", "catalogue_proves_fibre_triviality"):
        block = src[src.index(f"def {name}() -> Bool:"):]
        assert "return False" in block.split("\n\n")[0]
    assert not re.search(r"\bFloat(?:16|32|64|Literal)?\b", src)
    assert not re.search(r"(?<![\w.])\d+\.\d", src)


def test_regime_correspondence_binds_the_catalogue_symbols():
    spec = tomllib.loads(text(ROOT / "spec" / "regime_correspondences.toml"))
    entry = next(c for c in spec["correspondence"] if c["id"] == "misiurewicz-exact-type")
    assert "parameter location" in entry["does_not_inherit"]
    assert "fibre triviality" in entry["does_not_inherit"]
    for symbol in entry["symbols"]:
        path, name = symbol.split("::")
        assert path == "src/misiurewicz_catalogue.mojo" and f"def {name}(" in text(SRC)
    assert text(SRC).count("# Regime correspondence: misiurewicz-exact-type") == len(entry["symbols"])


# --- the reference model --------------------------------------------------------


def test_exact_type_is_read_off_the_reduced_denominator():
    assert mc.exact_type(1, 2) == (1, 1) and mc.exact_type(1, 6) == (1, 2)
    assert mc.exact_type(1, 3) == (0, 2) and mc.exact_type(2, 6) == (0, 2)
    assert mc.exact_type(0, 1) == (0, 1) and mc.exact_type(1, 4) == (2, 1)
    assert mc.misiurewicz(1, 2) and mc.misiurewicz(1, 6) and not mc.misiurewicz(1, 3)


def test_the_type_agrees_with_iterating_the_doubling_map():
    for den in range(1, 120):
        for num in range(den):
            expected = mc.exact_type(num, den)
            # Doubling is well defined on Z/den, and two states are the same
            # angle exactly when their numerators agree, so the first repeat
            # gives the preperiod and the period directly.
            seen: dict[int, int] = {}
            point, step = num % den, 0
            while point not in seen:
                seen[point] = step
                point, step = (2 * point) % den, step + 1
            assert expected == (seen[point], step - seen[point]), (num, den)


def test_out_of_range_addresses_are_refused():
    for num, den in ((1, 0), (5, 3), (-1, 4), (3, 3), (1, mc.MAX_CATALOGUE_DENOMINATOR + 1)):
        assert mc.exact_type(num, den) is None


def test_pinned_catalogues():
    assert mc.main() == 0
    assert mc.catalogue(1, 1) == [1] and mc.catalogue_denominator(1, 1) == 2
    assert mc.catalogue(2, 1) == [1, 3] and mc.catalogue_denominator(2, 1) == 4
    assert mc.catalogue(1, 2) == [1, 5] and mc.catalogue_denominator(1, 2) == 6
    assert mc.catalogue(1, 3) == [1, 3, 5, 9, 11, 13] and mc.catalogue_denominator(1, 3) == 14
    assert len(mc.catalogue(2, 3)) == 12 and len(mc.catalogue(3, 3)) == 24


def test_the_counting_identity_matches_the_enumeration():
    for preperiod in range(1, 8):
        for period in range(1, 8):
            if mc.catalogue_denominator(preperiod, period) < 0:
                continue
            assert len(mc.catalogue(preperiod, period)) == mc.catalogue_count(preperiod, period)


def test_the_count_doubles_with_the_preperiod_and_is_moebius_in_the_period():
    for period in range(1, 7):
        base = mc.catalogue_count(1, period)
        assert base == sum(mc.moebius(period // d) * ((1 << d) - 1) for d in range(1, period + 1) if period % d == 0)
        for preperiod in range(1, 6):
            assert mc.catalogue_count(preperiod, period) == (1 << (preperiod - 1)) * base


def test_moebius_values():
    assert [mc.moebius(n) for n in (1, 2, 3, 4, 5, 6, 8, 30)] == [1, -1, -1, 0, -1, 1, 0, -1]


def test_types_and_denominators_beyond_the_bounds_are_refused():
    assert mc.catalogue_denominator(0, 2) == -1 and mc.catalogue_denominator(1, 0) == -1
    assert mc.catalogue_denominator(1, mc.MAX_TYPE_INDEX + 1) == -1
    assert mc.catalogue_denominator(1, 20) == -1
    assert mc.catalogue_count(0, 1) == -1 and mc.catalogue(0, 1) == []


def test_mojo_smoke_pins_the_same_instances():
    src = text(SRC)
    for fragment in ("var one_three: List[Int] = [1, 3, 5, 9, 11, 13]", "catalogue_denominator(1, 3) != 14",
                     "catalogue_count(2, 3) != 12", "catalogue_count(3, 3) != 24", "catalogue_matches_count(l, k)"):
        assert fragment in src
    assert "misiurewicz_catalogue_smoke" in text(ROOT / "src" / "smoke_tests.mojo")
