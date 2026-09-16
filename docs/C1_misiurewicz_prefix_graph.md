# C1 Misiurewicz prefix graphs and the obstruction extractor

Status: definition-level finite extractor with an executable negative control; no theorem-status change.

This note delivers round-two item R5 of `docs/cross-pollination-round-two-2026-09-16.md`, section N3. It runs the obstruction extractor of the Pisot overlap route on the finite graphs the exact-type catalogue of `docs/C1_misiurewicz_catalogue.md` supplies, and it is what round-one B6 was the prerequisite for.

## Terminology declaration: prefix obstruction

Genealogy: This is the recurrent-core normal form that `larsbx/pisot-substitution-conjecture-research` extracts from its overlap graph (`docs/p1-overlap-minimal-obstruction-2026-09-14.md`, `mojo/psc/overlap_obstruction.mojo`), and abstractly the finite obstruction object route F1 asks for in `docs/C1_F1_obstruction_extraction.md`. The graph-theoretic content, a backward productivity fixpoint followed by sink components, is standard.

Bridge claim: Definition-only project term. A `prefix obstruction` of a separator prefix is a sink component of the pairs that no iterate of doubling separates. It is a statement about one finite prefix graph, not about any parameter and not about any fibre.

Known leaks: One prefix is not every prefix. An empty obstruction set at a prefix says nothing about a finer one, and persistent non-separation quantifies over all of them. A refusal at the bound is not an empty obstruction set, and the two must never be read alike.

Use discipline: Use in C1 files or with a pointer to this registry, and only for sink components of one named prefix. A prefix obstruction does not locate a parameter, does not decide a fibre, and does not settle C1.

## The pipeline

For an exact type `(l, k)` with denominator `den`, the graph is built in `Z/den`:

| Stage | Object |
| --- | --- |
| vertices | the forward orbit closure of the catalogue under doubling |
| pairs | the unordered non-diagonal pairs of vertices |
| productive | separated by the prefix now, or with a productive successor |
| nonproductive | the rest: the pairs no iterate ever separates |
| sinks | the cycles of the nonproductive set |
| dichotomy | each cycle is a boundary or an interior obstruction |

Two points are separated by the prefix exactly when some two-ray separator puts them on opposite sides, which is the side-signature test of `docs/C1_separated_pair_density.md`.

Productivity is computed backwards from the separated pairs, exactly as the overlap route computes it backwards from its coincidences. **Forward closedness of the nonproductive set is then a lemma rather than a computation**: a nonproductive pair cannot have a productive successor, because a separation reached from the successor is reached from the pair one step earlier. Computing a forward closure instead would be wrong, since it would admit images that the prefix does separate.

Doubling is a function, so the pair graph has out-degree at most one and every component falls into exactly one cycle. The sink components are therefore the cycles, and no strongly-connected-component search is needed. This is the one place the mirror is simpler than the overlap route, whose graph branches and which runs an iterative Tarjan pass.

## Merging pairs

Two points with the same image, that is differing by `den / 2`, give a pair with no successor. Such a pair is never separated, so it is nonproductive. Counting it productive would be the substantive error available here: those two addresses are precisely the ones doubling can never tell apart, so they are an obstruction and not a discharge.

Merging pairs are transient and never sinks, and they are counted separately. They are also why the obstruction-free test is the whole nonproductive set rather than its sinks: over the denominator `4`, the type `(2, 1)` with no separator at all has six nonproductive pairs, two of them merging, and no cycle whatsoever.

## The dichotomy

The split transfers term by term from the overlap route:

| Overlap route | Here |
| --- | --- |
| aligned obstruction: a child start coincides, some child has zero shift | **boundary**: some point on the cycle is a separator endpoint, so the object may lie on the separation line itself, the `BoundaryEqualityCandidate` of `docs/C1_canonical_carrier_content.md` |
| strict-zipper obstruction: no zero-shift child, one side advances at each step | **interior**: no separator boundary is ever hit, so the prefix is not fine enough, which is `CarrierTooCoarse` |

The dichotomy is a property of the prefix, not of the cycle. Over the denominator `14`, the period-three orbit `3/7 -> 6/7 -> 5/7` is an interior obstruction for the prefix with first rays `1, 2, 3`, and the same cycle becomes a boundary obstruction for the prefix with first rays `1, 2, 5`, because that prefix makes `6/14` an endpoint.

No PF-critical or full-rank check appears here, for the same reason it appears nowhere in the overlap route: those are proved invariants of what the extractor returns, not filters the extractor applies.

## The negative control

With its full separator prefix, consecutive points of the forward closure, every exact type within the bound leaves nothing undecided and no obstruction. That is the executable negative control section N3 promises, and it is checked for all 29 types within the bound in both the Mojo smoke target and the Python reference.

It is a negative control and not a theorem: it says the finest prefix this catalogue supplies decides every pair on that class, which is what the imported tag `KnownTrivialFiberClass` would lead one to expect, and it is evidence of nothing about a class that tag does not cover.

## Bounds and fail-closed behaviour

One constant governs the graph. Vertices live in `Z/den`, so `MAX_PREFIX_GRAPH_DENOMINATOR` caps the vertex count and the pair count together, and the Python reference carries the same constant so the two agree on every refusal. Of the 64 exact types with both indices at most eight, 29 are within the bound and 35 are past it.

A denominator past the bound, a mismatched or malformed separator list, and an out-of-range point are refused before any graph is built. **A refusal is never an empty answer.** An empty obstruction set is a positive verdict about a complete graph, so `obstruction_free` requires acceptance, and a bounded search that failed never reads as a clean verdict. This is UW-2: a bounded failed search is not persistent evidence.

## Non-claims

`obstruction_free_proves_fibre_triviality`, `extractor_decides_persistent_nonseparation`, and `bounded_refusal_is_evidence_of_no_obstruction` all return `False`. This note does not claim:

- that C1 is proved, or that any fibre is trivial;
- that an empty obstruction set at one prefix implies one at a finer prefix;
- that a prefix obstruction locates a parameter or identifies a fibre;
- that the extractor decides persistent non-separation, which quantifies over every prefix.

## Next target

The extractor reports sink components by kind. The next local target is to emit the smallest interior obstruction as a replayable witness rather than a count, which is the countermodel-retention step the overlap route also lists as future work.
