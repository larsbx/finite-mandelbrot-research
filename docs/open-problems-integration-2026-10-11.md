# Mandelbrot open-problems survey: integration and research obligations

Status: literature intake, reviewed 2026-10-11. This note routes the supplied
survey into existing work; it does not establish new theorem imports or alter
C1 proof status. C1 remains priority zero under
[C1 proof criteria](C1_proof_definition_and_priority.md), and
[proof/c1/records.toml](../proof/c1/records.toml) remains authoritative.

## Source and review scope

The [supplied survey](sources/mandelbrot-open-problems-survey-2026-10.txt) is
preserved byte-for-byte as a plain-text external research input. The archive
is not governed project prose; the reviewed integration is. Original filename:
`Open Problems and Conjectures on the Mandelbrot Set_ A Research-.md`.
SHA-256: `808e38137448517be73f06f797b79ac636fbfdbca6fb6e23660c6a5e9769e51c`.
Its October 2026 status assertions, diagrams and estimates are source claims,
not repository-certified conclusions. Read them with the corrections below.

Primary-source checks in this intake covered the arXiv abstracts and version
records for Dudko's survey, Dudko–Lyubich, Kahn–Kapiamba–Lyubich and Kapiamba.
This is an abstract-level review, not an independent proof audit. The remaining
arithmetic, area, computability and generalization claims await statement-level
review; their presence in the archive does not approve them.

## Reviewed literature and corrections

| Source | Check on 2026-10-11 | Repository consequence |
| --- | --- | --- |
| Dudko, [survey, 2512.24171](https://arxiv.org/abs/2512.24171) | Bibliographic record checked; the uploaded note's specific Problems 4.3/4.4 require full-text statement review | Use as a candidate map of the residual frontier, not a completed reduction |
| Dudko–Lyubich, [2309.02107v3](https://arxiv.org/abs/2309.02107v3), 2025-12-29 | Abstract states a priori bounds and MLC for infinitely renormalizable quadratic parameters of bounded type | Candidate restricted trivial-fiber import; certify membership in the stated class before use |
| Kahn–Kapiamba–Lyubich, [2606.27272v1](https://arxiv.org/abs/2606.27272v1), 2026-06-25 | Abstract states bounds and MLC for a primitive class approaching the cusp | Candidate additional restricted import; exact combinatorial hypotheses and dependencies still need pinning |
| Kapiamba, [2401.00795v2](https://arxiv.org/abs/2401.00795v2) | Withdrawn 2025-01-03 and combined into 2103.03211 | Do not cite the withdrawn record as the current standalone result |
| Kapiamba, [2103.03211v4](https://arxiv.org/abs/2103.03211v4), 2025-01-13 | Current combined paper: near-parabolic geometry and a quadratic Pommerenke–Levin–Yoccoz inequality | Route limb geometry to the companion project; extract the precise scope before invoking a limb bound |

Further corrections to how the survey is used:

- Keep density of hyperbolicity (a density assertion in parameter space) distinct
  from the stronger-looking equality written in the survey for the interior of
  the Mandelbrot set. Do not import the survey's DH/NILF equivalence chain
  without exact statements, hypotheses and a proof of each required arrow.
- Fiber triviality uses the specified separation-line framework. Merely sharing
  rational lamination data or having every ray land is not an accepted equality
  adapter here. Landing and continuous extension must be distinguished.
- Parameter local connectivity and dynamical Julia-set local connectivity are
  different predicates; no generic implication is registered by this intake.
- Announced MLC along veins, unpublished dependencies, and the survey's two
  title-only 2026 papers remain unverified inputs.
- Fisher–Hill bounds described as rigorous only up to double precision are not
  fully certified rational bounds. Pixel estimates and component sums without
  error control are numerical evidence. No best-current-area ranking is adopted.
- A finite-field factorization or orbit census does not prove characteristic-zero
  irreducibility, equidistribution, classical membership or fiber triviality.

## Fit to the current research program

| Survey topic | Existing home | Concrete obligation and acceptance boundary |
| --- | --- | --- |
| MLC, rigidity, renormalization | C1 residual closure | Extract class hypotheses, theorem/version and dependency list; supply a membership witness and the classical fiber adapter before accepting a restricted exit |
| Unbounded satellite and near-molecule cases | ResidualClosureNoMissingLinks | Record coverage and complementary cases explicitly; finite experiments cannot eliminate the generic missing-link exit |
| Gleason/Misiurewicz arithmetic | [Multiset bridge](multiset-bridge-program.md) | Extend exact-type divisor certificates, separating integral division, modular squarefreeness, irreducibility and embedding localization |
| Core entropy | [Existing literature gate](hubbard-core-entropy-literature-gate-2026-09-17.md) | Preserve primitive/imprimitive/reducible strata and exact algebraic growth rates; this survey does not override the gate or certify a new census |
| Computability and area | Three-valued certificate renderer, ROADMAP Phase 3 | Keep unresolved boxes UNKNOWN; a future area enclosure needs certified IN/OUT boxes, disjoint accounting and rational endpoints |
| Limb/bulb geometry | [Bulb/Ford companion repository](https://github.com/larsbx/mandelbrot-bulbs-and-ford-circles-research) | Distinguish whole-limb diameter from bulb shape and radius; local coefficient certificates do not establish uniform global limb estimates |
| Finite-field statistics | Arithmetic shadow layer | Declare primes, sample domain, weights and exact orbit invariants; retain the characteristic-zero bridge obligations |
| Poonen, arboreal Galois, higher-degree loci, DAO | Deferred literature context | No new implementation track or theorem dependency until a concrete need and primary-source review are recorded |

## Ordered next obligations

1. Extract statement-level records for the bounded-type and parabolically
   bounded primitive MLC results, including all unpublished dependencies.
   Specify how an admissible representative supplies the necessary class witness.
2. Connect those restricted conclusions to the existing fiber-definition adapter
   and test whether they close a named residual exit. Record the uncovered
   complement; keep generic residual closure open.
3. Review Dudko's Problems 4.3/4.4 in full text against the existing residual
   directive work. Any useful reformulation must preserve the original hypotheses
   and explicitly identify the still-open theorem.
4. Continue exact-type divisor refinement and embedding/localization work through
   the existing multiset bridge. Treat general irreducibility as a separate target.
5. Reuse the existing core-entropy gate and companion bulb/Ford register rather
   than creating duplicate censuses or rewriting their evidence tiers.

A proposed import is ready only when its exact statement, version, hypotheses,
external dependencies, finite membership witness, adapter and affected ledger
record are all reviewable. Any proof-state update must go through the canonical
records and regenerated surfaces. This intake introduces no accepted theorem tag.
