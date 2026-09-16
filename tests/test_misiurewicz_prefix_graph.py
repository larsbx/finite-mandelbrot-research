"""Conformance of the obstruction extractor with docs/C1_misiurewicz_prefix_graph.md."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import misiurewicz_catalogue_reference as mc  # noqa: E402
import misiurewicz_prefix_graph_reference as pg  # noqa: E402

DOC = ROOT / "docs" / "C1_misiurewicz_prefix_graph.md"
SRC = ROOT / "src" / "C1_misiurewicz_prefix_graph.mojo"

DEN13 = 14  # the denominator of exact type (1, 3)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def seps(*pairs: tuple[int, int]) -> list[tuple[int, int]]:
    return list(pairs)


# --- documentation and governance ----------------------------------------------


def test_term_is_declared_with_genealogy_and_leaks():
    body = text(DOC)
    assert body.splitlines()[2].startswith("Status:")
    assert "Terminology declaration: prefix obstruction" in body
    for field in ("Genealogy:", "Bridge claim:", "Known leaks:", "Use discipline:"):
        assert field in body
    assert "Definition-only" in body
    assert "prefix obstruction" in text(ROOT / "docs" / "terminology-registry.md")


def test_non_claims_return_false_in_mojo():
    src = text(SRC)
    for name in ("obstruction_free_proves_fibre_triviality",
                 "extractor_decides_persistent_nonseparation",
                 "bounded_refusal_is_evidence_of_no_obstruction"):
        block = src[src.index(f"def {name}() -> Bool:"):]
        assert "return False" in block.split("\n\n")[0]
    assert not re.search(r"\bFloat(?:16|32|64|Literal)?\b", src)
    assert not re.search(r"(?<![\w.])\d+\.\d", src)


def test_regime_correspondence_binds_the_extractor_symbols():
    spec = tomllib.loads(text(ROOT / "spec" / "regime_correspondences.toml"))
    entry = next(c for c in spec["correspondence"] if c["id"] == "misiurewicz-prefix-obstruction")
    for absent in ("fibre triviality", "persistent non-separation", "parameter location"):
        assert absent in entry["does_not_inherit"]
    for symbol in entry["symbols"]:
        path, name = symbol.split("::")
        assert path == "src/C1_misiurewicz_prefix_graph.mojo" and f"def {name}(" in text(SRC)
    tag = "# Regime correspondence: misiurewicz-prefix-obstruction"
    assert text(SRC).count(tag) == len(entry["symbols"])


def test_the_two_implementations_share_one_bound():
    assert f"comptime MAX_PREFIX_GRAPH_DENOMINATOR = {pg.MAX_PREFIX_GRAPH_DENOMINATOR}" in text(SRC)


# --- the graph ------------------------------------------------------------------


def test_forward_closure_is_closed_under_doubling_and_contains_the_seed():
    for preperiod in range(1, 6):
        for period in range(1, 6):
            den = mc.catalogue_denominator(preperiod, period)
            if den < 0 or den > pg.MAX_PREFIX_GRAPH_DENOMINATOR:
                continue
            seed = mc.catalogue(preperiod, period)
            closure = pg.forward_closure(seed, den)
            assert set(seed) <= set(closure)
            assert {(2 * x) % den for x in closure} <= set(closure)
            assert closure == sorted(set(closure))


def test_exchanging_a_separators_rays_names_the_complementary_side():
    for point in range(DEN13):
        assert pg.side(point, (3, 9), DEN13) != pg.side(point, (9, 3), DEN13)


def test_separation_is_the_side_signature_test():
    prefix = seps((1, 2), (5, 6))
    for a in range(DEN13):
        for b in range(DEN13):
            same = pg.signature(a, prefix, DEN13) == pg.signature(b, prefix, DEN13)
            assert pg.separated(a, b, prefix, DEN13) is not same


def test_a_pair_merges_exactly_when_its_points_differ_by_half():
    for a in range(DEN13):
        for b in range(a + 1, DEN13):
            merges = pg.successor((a, b), DEN13) is None
            assert merges == ((b - a) % DEN13 == DEN13 // 2)


# --- the extractor --------------------------------------------------------------


def test_the_nonproductive_set_is_forward_closed():
    # The lemma the pipeline rests on, checked rather than assumed: a
    # nonproductive pair never has a productive successor.
    for prefix in (seps(), seps((2, 3)), seps((1, 2)), seps((1, 2), (2, 3), (5, 6))):
        vertices = pg.forward_closure(mc.catalogue(1, 3), DEN13)
        bad = pg.nonproductive(vertices, prefix, DEN13)
        for pair in bad:
            after = pg.successor(pair, DEN13)
            assert after is None or after in bad, (prefix, pair)


def test_a_merging_pair_is_nonproductive_not_productive():
    # Two addresses with a common image are exactly the ones doubling can never
    # tell apart, so they are an obstruction rather than a discharge.
    vertices = pg.forward_closure(mc.catalogue(2, 1), 4)
    bad = pg.nonproductive(vertices, [], 4)
    merging = [p for p in bad if pg.successor(p, 4) is None]
    assert merging and all(p in bad for p in merging)


def test_nonproductive_is_monotone_under_refining_the_prefix():
    vertices = pg.forward_closure(mc.catalogue(1, 3), DEN13)
    coarse = pg.nonproductive(vertices, seps((1, 2)), DEN13)
    finer = pg.nonproductive(vertices, seps((1, 2), (2, 3)), DEN13)
    assert finer <= coarse


def test_sink_cycles_are_cycles_and_partition_no_pair_twice():
    vertices = pg.forward_closure(mc.catalogue(1, 3), DEN13)
    bad = pg.nonproductive(vertices, seps((1, 2)), DEN13)
    cycles = pg.sink_cycles(bad, DEN13)
    seen: set[tuple[int, int]] = set()
    for cycle in cycles:
        assert set(cycle) <= bad
        for index, pair in enumerate(cycle):
            assert pg.successor(pair, DEN13) == cycle[(index + 1) % len(cycle)]
        assert not (set(cycle) & seen)
        seen |= set(cycle)


def test_the_pinned_thin_prefix_instance():
    found = pg.extract(mc.catalogue(1, 3), seps((2, 3)), DEN13)
    assert (found.vertices, found.undecided, found.nonproductive) == (12, 55, 17)
    assert (found.merging, len(found.boundary), len(found.interior)) == (5, 0, 1)
    # The interior cycle is the period-three orbit 3/7 -> 6/7 -> 5/7.
    assert found.interior == (((6, 10), (6, 12), (10, 12)),)
    assert not found.obstruction_free


def test_the_dichotomy_is_a_property_of_the_prefix_not_of_the_cycle():
    interior = pg.extract(mc.catalogue(1, 3), seps((1, 2), (2, 3), (3, 4)), DEN13)
    boundary = pg.extract(mc.catalogue(1, 3), seps((1, 2), (2, 3), (5, 6)), DEN13)
    assert interior.cycles == boundary.cycles          # the same cycle
    assert interior.nonproductive == boundary.nonproductive
    assert (len(interior.interior), len(interior.boundary)) == (1, 0)
    assert (len(boundary.boundary), len(boundary.interior)) == (1, 0)


def test_a_nonproductive_set_can_be_entirely_transient():
    # Six nonproductive pairs, two merging, and no cycle at all: the reason the
    # obstruction-free test is the whole set rather than its sinks.
    bare = pg.extract(mc.catalogue(2, 1), [], 4)
    assert (bare.nonproductive, bare.merging, len(bare.cycles)) == (6, 2, 0)
    assert not bare.obstruction_free


def test_multiple_sinks_are_all_retained():
    # The case the overlap route's Python oracle covers and its Mojo suite does
    # not: several disjoint cycles must each be reported.
    vertices = pg.forward_closure(mc.catalogue(1, 3), DEN13)
    bad = pg.nonproductive(vertices, seps((1, 2)), DEN13)
    assert len(pg.sink_cycles(bad, DEN13)) == 5
    found = pg.extract(mc.catalogue(1, 3), seps((1, 2)), DEN13)
    assert len(found.boundary) == 4 and len(found.interior) == 1


# --- the negative control and fail-closed behaviour ------------------------------


def test_the_full_prefix_leaves_no_obstruction_on_every_type_in_range():
    assert pg.main() == 0
    checked = 0
    for preperiod in range(1, 9):
        for period in range(1, 9):
            found = pg.extract_catalogue(preperiod, period)
            if not found.accepted:
                continue
            assert found.obstruction_free and found.undecided == 0, (preperiod, period)
            checked += 1
    assert checked == 29


def test_the_smoke_target_pins_the_same_instances():
    src = text(SRC)
    for fragment in ("if checked != 29 or bounded != 35:",
                     "if thin.vertices != 12 or thin.undecided != 55 or thin.nonproductive != 17:",
                     "if thin.merging != 5 or thin.boundary != 0 or thin.interior != 1:",
                     "if not bare.accepted() or bare.nonproductive != 6 or bare.merging != 2:",
                     "var expected: List[Int] = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]"):
        assert fragment in src
    assert "misiurewicz_prefix_graph_smoke" in text(ROOT / "src" / "smoke_tests.mojo")


def test_a_refusal_is_never_an_empty_obstruction_set():
    refused = pg.rejected_extraction()
    assert refused.rejected and not refused.accepted
    assert not refused.obstruction_free      # UW-2: a bounded failure is not evidence
    assert refused.nonproductive == 0        # and it carries no counts either way


def test_malformed_and_out_of_range_inputs_are_refused():
    cat = mc.catalogue(1, 3)
    assert pg.extract(cat, seps((3, 3)), DEN13).rejected          # a separator needs two rays
    assert pg.extract(cat, seps((1, DEN13)), DEN13).rejected      # ray out of range
    assert pg.extract(cat, seps((-1, 2)), DEN13).rejected
    assert pg.extract(cat, [], 0).rejected                        # no denominator
    assert pg.extract([99], [], DEN13).rejected                   # seed out of range
    assert pg.extract([], [], DEN13).rejected                     # empty seed
    assert pg.extract(cat, [], pg.MAX_PREFIX_GRAPH_DENOMINATOR + 1).rejected
    assert pg.extract_catalogue(4, 5).rejected                    # denominator 496


def test_counts_past_the_bound_are_refusals_not_passes():
    bounded = [(l, k) for l in range(1, 9) for k in range(1, 9)
               if mc.catalogue_denominator(l, k) >= 0 and pg.extract_catalogue(l, k).rejected]
    assert len(bounded) == 35
    assert all(mc.catalogue_denominator(l, k) > pg.MAX_PREFIX_GRAPH_DENOMINATOR for l, k in bounded)


def test_the_non_claims_hold_in_the_reference_too():
    assert not pg.obstruction_free_proves_fibre_triviality()
    assert not pg.extractor_decides_persistent_nonseparation()
