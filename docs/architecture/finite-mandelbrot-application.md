# Applying estate repository template v1 to finite Mandelbrot

Status: first consumer; boundary-first migration.

This repository is intentionally the first adopter because its current tree already
contains every important estate role: canonical Mojo kernels, claim/proof state,
Python references and audits, Julia oracle/spike lanes, generated ledgers, vendored
packages, schemas, conformance tests, research documentation, and a paper.

No mathematical claim changes in this adoption.

## Current to target map

| Authority plane | Current location | Target organization |
| --- | --- | --- |
| policy | root TOML manifests | `policy/` |
| canonical kernel | `src/` | `kernel/mojo/<domain>/` |
| C1 proof state | `ledger.json`, `tla/`, generated C1 surfaces | `proof/c1/` |
| mathematical references | `tools/*_reference.py`, selected oracle scripts | `reference/python/<domain>/` |
| research oracles | `oracles/julia/` | stays `oracles/julia/` |
| experiments | `spikes/julia/` | `experiments/julia/` |
| schemas | `spec/`, `.polyglot/*.schema.json` | `schemas/` |
| conformance | `tests/`, polyglot vectors | `conformance/` plus implementation tests |
| vendored source | nested under `src/` and `tools/` | `vendor/` after import-boundary work |
| repository tooling | `tools/audit_*.py`, generators | stays `tools/` |
| documentation | flat `docs/` | categorized under `docs/` |
| publication | `paper/` | stays `paper/` |

## Why this is transitional

The current Mojo compile closure imports modules from `src/`, and vendored digests
pin bytes at their existing paths. Moving those files in the template-adoption PR
would mix architecture declaration with import rewrites and vendor re-pinning.

Therefore v1 adds the authority model first and keeps all existing paths live.

## Follow-on migrations

### 1. Declarative C1 proof plane — implemented source boundary

The authoritative C1 claim-state data now lives in `proof/c1/records.toml`.
`tools/make_ledger.py` validates and renders it; the generator no longer embeds
the theorem-status table. Generated surfaces remain at their historical paths
for now so this slice does not mix source-of-truth extraction with path moves.

The eventual fully migrated shape remains:

```text
proof/c1/
  records.toml                 # canonical claim/proof record data
  imports/
  models/tla/
  generated/
    ledger.json
    ledger.md
    relationship-graph.json
    mojo/
```

Generators contain mechanism, not the authoritative theorem-status table. This first migration satisfies that rule; moving generated projections under `proof/c1/generated/` is deferred until consumers can move atomically.

### 2. Reference/tool split — implemented

Independently written mathematical semantics now live under `reference/python/`
by domain. Repository maintenance, audits and generators remain under `tools/`.
Historical `tools/*_reference.py` and `tools/*_oracle.py` entrypoints are thin
compatibility shims only; CI and new tests target the reference plane directly.

### 3. Kernel namespaces

Replace the flat `C1_*.mojo` pseudo-namespace with domain directories such as:

```text
kernel/mojo/c1/
  separator/
  carrier/
  residual/
  theorem_tags/
```

This is a semantic-preserving import migration.

### 4. Vendor boundary

Make finite-math-kernels packages visibly external. Do not move pinned bytes until
the Mojo/Python import and digest checks can preserve the exact vendor contract.

### 5. CI authority lanes

Split the monolithic core audit into policy, kernel, proof, reference/oracle, paper,
and final integration gates. A failing lane should identify which authority plane
is red.

## Invariants during migration

- Mojo remains the current canonical executable certificate/proof-object checker.
- Julia and Python remain non-authoritative for acceptance.
- C1 status cannot change as a side effect of a path move.
- Imported analytic theorem assumptions remain explicit.
- Vendored digest checks remain fail-closed.
- Generic boundary completeness remains open unless separately proved.
