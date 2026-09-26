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

### 1. Declarative C1 proof plane

Move claim-state data out of generator implementation. The intended shape is:

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

Generators should contain mechanism, never the authoritative theorem-status table.

### 2. Reference/tool split

Move independently written mathematical semantics from `tools/` to
`reference/python/`. Keep repository maintenance, audits and generators in
`tools/`.

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
