# Shared finite-math kernel migration

Status: implemented consumer migration; no theorem-status change.

finite-mandlebrot-research vendors `finite_exact/` from `larsbx/finite-math-kernels` at the full
commit recorded in `vendored.toml`. The checker is itself vendored from the
same upstream (`vendor/python/vendoring/check_vendored_sync.py`, `pixi run
vendored`): it verifies every vendored file by SHA-256 in CI, rejects an
unpinned source file inside a vendored package directory, and checks that the
`finite-math-kernels` `[[dep]]` pin in `ESTATE.toml` is the digest derived from
`vendored.toml`. After copying a package from upstream, `check_vendored_sync.py
pin NAME COMMIT` re-pins its digests and re-derives that pin (a new package is
first added to `vendored.toml` with its name, repository, root, and an empty
`[package.files]` table); `check_vendored_sync.py estate` re-derives the pin
alone. Arithmetic consumers import the
package-qualified modules under `vendor/mojo/finite_exact/`; the former root-level
implementations were removed.

The same pin also vendors the monorepo's `substitution_dynamics` tuning,
directive-prefix, and column-coincidence modules under
`vendor/mojo/substitution_dynamics/`, consumed by `kernel/mojo/c1/residual/residual_directive_carrier.mojo`
(`docs/C1_residual_directive_carrier.md`); the balanced-pair and automaton
modules are not vendored.

This changes ownership, not mathematical semantics:

- `BigZ` and `Q` remain exact, unbounded, and fail closed;
- interval predicates remain conservative and distinct from exact acceptance;
- certificate acceptance remains a consumer responsibility;
- C1 and every source-pending theorem dependency remain unresolved unless a
  separate proof record says otherwise.

The old standalone library repositories may be archived only after the PSC
consumer migration is merged and repository-wide reference checks show no
live pin to them.

