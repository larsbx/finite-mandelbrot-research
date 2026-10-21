# Roadmap

Status: current as of 2026-10-21.

This roadmap separates two kinds of work that must not be conflated:

1. **C1 proof work**, whose highest-priority mathematical obligation is
   `ResidualClosureNoMissingLinks`.
2. **Finite-certificate engineering**, whose next c=-2 hardening target is
   `CanonicalFiniteCertificateIncidenceReplay`.

Completing a local certificate milestone does not discharge C1, generic MLC,
all-fiber triviality, or the residual global closure obligation.

## Phase 0 — Research scaffold

- [x] State the finite-regime thesis.
- [x] Separate finite certificates from analytic theorem tags.
- [x] Add a worked algebraic smoke test at `c = -2`.
- [x] Make Mojo the canonical executable finite-checker language.
- [x] Separate canonical Mojo, proof records, reference implementations, and
      documentation into explicit authority planes.
- [ ] Add a computed multi-ray stress test with verified interval margins.

## Phase 1 — Certificate calculus

The finite certificate calculus is operational for the c=-2 path and includes:

- [x] critical-orbit polynomial recurrence
      `Q_0 = 0`, `Q_{n+1} = Q_n^2 + C`;
- [x] exact return-polynomial and squarefree/exact-type reasoning;
- [x] normalized BigZ-backed rational arithmetic;
- [x] rational-endpoint interval and Krawczyk replay;
- [x] same-box forbidden-collision checks;
- [x] rational ray-address combinatorics;
- [x] source-scoped theorem-tag imports;
- [x] proof-grade rational landing-target association for
      `c=-2`, address `1/2`, exact type `(2,1)`;
- [x] proof-grade Misiurewicz trivial-fiber classification for that same
      source-scoped instance;
- [x] finite incidence packaging as explicit vertices rather than analytic
      point primitives;
- [ ] canonical serialization and deterministic replay of the finite incidence
      package;
- [ ] acceptance-bearing complete certificate emission after that replay.

The completed theorem-tag milestones were integrated through PRs #19, #20,
#21, and #23. They establish the local c=-2 import chain only. They do not
promote a generic boundary theorem.

## Phase 2 — Prototype verifier

The prototype verifier is now a compiler-wired Mojo checker rather than a
language-selection exercise.

Current layers:

1. [x] exact polynomial recurrence and factor/divisor checks;
2. [x] BigZ and normalized-Q arithmetic;
3. [x] rational interval arithmetic;
4. [x] complex Krawczyk and exact-type exclusion replays;
5. [x] rational-address dynamics;
6. [x] theorem-tag record/payload checking;
7. [x] finite incidence packaging;
8. [ ] canonical finite-incidence serialization and cross-process replay;
9. [ ] complete proof-grade certificate acceptance for the c=-2 exemplar.

### Immediate certificate-engineering target

```text
CanonicalFiniteCertificateIncidenceReplay
```

Acceptance criteria:

- define canonical bytes for the explicit finite incidence carrier;
- prove/replay deterministic encoding of the same package across processes;
- reject malformed, reordered, role-mismatched, or non-canonical encodings;
- bind the replay to the already accepted c=-2 theorem-tag payloads;
- keep C1 and `ResidualClosureNoMissingLinks` explicitly false;
- only then permit the c=-2 finite-certificate gate to become
  acceptance-bearing.

## Phase 3 — Certified renderer bridge

Integrate the certificate calculus with a three-valued renderer:

- [ ] escape certificates for `OUT` boxes;
- [ ] attracting-cycle or bulb/cardioid certificates for `IN` boxes;
- [ ] Misiurewicz/parabolic landing certificates for algebraic boundary anchors;
- [ ] `UNKNOWN` boxes for unresolved generic boundary regions;
- [ ] optional area enclosures based only on disjoint certified IN/OUT boxes.

Renderer output is never proof evidence by itself.

## Phase 4 — Fiber/MLC reduction and C1

C1 remains `PRIORITY_ZERO`. The authoritative completion criterion is
`docs/C1_proof_definition_and_priority.md`.

The highest-priority open mathematical block is:

```text
ResidualClosureNoMissingLinks
```

The required residual implication is still:

```text
PersistentNonSeparation(A,B)
  => FiniteSeparation(A,B)
     or BoundaryEquality(A,B)
     or EstablishedTrivialFiberTag(A,B)
```

with no remaining `MissingTheoremCatalogueLink` exit.

Current priority order:

1. `ResidualClosureNoMissingLinks`;
2. `SeparatorCatalogueAdequacyProofObjects`;
3. `FiberDefinitionAdapterProofObject`;
4. `C1FinalProofObject`;
5. performance work needed by those proof objects.

Local Misiurewicz, parabolic, hyperbolic, bounded-search, renderer, or finite
certificate successes are insufficient to close this phase.

## Phase 5 — Formalization and implementation authority

The repository no longer has an open choice among Rust, Zig, Python, or a
proof assistant for the primary executable checker.

Current authority split:

- **Mojo** — canonical executable finite arithmetic, certificate kernels, and
  finite theorem-kernel checking;
- **Python** — non-authoritative reference oracles, audits, generators, and CI
  support;
- **declarative proof records / generated proof surfaces** — repository proof
  state and dependency tracking;
- **external analytic literature** — explicit theorem-tag imports with checked
  source, scope, assumptions, and adapters.

A Lean/Rocq formalization remains a possible later verification layer, but it
is not a prerequisite for the current certificate or C1 roadmap unless a
specific proof obligation is assigned to it.

## Parallel algebraic multiset track

Continue the exact critical-orbit divisor and finite-field shadow program
without treating it as a substitute for the C1 route.

Current established example:

- `D^{exact}_{4,1} = div_0(F_7)` has seven distinct algebraic roots of exact
  critical-orbit type `(4,1)`.

Remaining bridge work includes complex-embedding/localization handles and any
additional theorem needed to connect finite-field or basin-cardinality
statistics back to characteristic-zero Mandelbrot claims.

## October 2026 literature obligations

The [survey integration](docs/open-problems-integration-2026-10-11.md) keeps an
ordered review queue under the existing C1 priority:

1. restricted MLC theorem statements and exact class witnesses;
2. residual coverage and adapter obligations;
3. algebraic localization and existing companion tracks.

New area, arithmetic-statistics, higher-degree, or companion investigations
remain gated by primary-source review and may not displace the priority-zero
C1 obligations.

## Completion discipline

Roadmap checkboxes record repository milestones, not mathematical conclusions
stronger than their named scope.

In particular:

- an accepted c=-2 certificate does not prove C1;
- a finite census does not prove generic MLC;
- a source citation without a checked theorem-tag payload is not executable
  evidence;
- an unresolved generic residual exit keeps C1 open.
