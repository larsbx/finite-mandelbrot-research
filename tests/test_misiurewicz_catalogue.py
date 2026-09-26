"""Conformance of the exact-type catalogue with docs/C1_misiurewicz_catalogue.md."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.python.c1 import misiurewicz_catalogue_reference as mc  # noqa: E402

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
            # Doubling is well defined on Z/den, and two states are the same
            # angle exactly when their numerators agree, so the first repeat
            # gives the preperiod and the period directly.
            seen: dict[int, int] = {}
            point, step = num % den, 0
            while point not in seen:
                seen[point] = step
                point, step = (2 * point) % den, step + 1
            assert mc.exact_type(num, den) == (seen[point], step - seen[point]), (num, den)


def test_an_accepted_type_is_not_a_promise_that_a_catalogue_holds_it():
    # The two bounds govern different things, and catalogueability is the
    # strictly stronger one. Both ways of failing it have a witness inside the
    # denominator bound, so acceptance must never be read as catalogueability.
    assert mc.exact_type(1, 58) == (1, 28) and not mc.catalogueable_type(1, 28)  # past the index bound
    assert mc.exact_type(1, 50) == (1, 20) and not mc.catalogueable_type(1, 20)  # past the denominator bound
    assert mc.catalogueable_type(1, 3) and mc.catalogue_denominator(1, 3) == 14
    # Wherever a catalogue does exist, every address it lists is accepted with
    # exactly that type: the reader and the enumeration agree on their overlap.
    for preperiod in range(1, 5):
        for period in range(1, 5):
            if not mc.catalogueable_type(preperiod, period):
                continue
            den = mc.catalogue_denominator(preperiod, period)
            for num in mc.catalogue(preperiod, period):
                assert mc.exact_type(num, den) == (preperiod, period), (num, den)


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


def test_the_mojo_catalogue_case_passes(mojo_smoke):
    """The Mojo catalogue is checked by running it, not by reading its source.

    `misiurewicz_catalogue_smoke` pins the same instances this module's
    reference pins -- the four catalogues, the counting identity, the two
    bounds, and the non-claims -- so a named pass here is the executable
    statement that Mojo and the reference agree."""
    assert mojo_smoke.returncode == 0, mojo_smoke.output
    assert mojo_smoke.case_passed("Misiurewicz exact-type catalogue")
    assert not mojo_smoke.failed, mojo_smoke.failed


def test_the_smoke_suite_names_every_case_it_runs(mojo_smoke):
    """A bare FAIL would not say which contract broke, so the suite names each
    case and keeps going after one fails."""
    assert mojo_smoke.total >= 50
    assert len(set(mojo_smoke.passed)) == len(mojo_smoke.passed)
    assert f"{mojo_smoke.total} cases, all passed." in mojo_smoke.output
