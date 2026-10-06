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
implementations were removed. The machine-integer gcd (`integer_gcd`) and the
base-ten renderer (`exact_decimal`), first written in this repository under
`kernel/mojo/arithmetic/`, now live upstream in `finite_exact` and are imported
from there; the local copies were removed.

The same pin also vendors the monorepo's `substitution_dynamics` tuning,
directive-prefix, and column-coincidence modules under
`vendor/mojo/substitution_dynamics/`, consumed by `kernel/mojo/c1/residual/residual_directive_carrier.mojo`
(`docs/C1_residual_directive_carrier.md`); the balanced-pair and automaton
modules are not vendored.

The smoke suite's named reporter is the vendored `mojo_smoke` package
(`vendor/mojo/mojo_smoke/report.mojo`); it replaced
`kernel/mojo/smoke/smoke_report.mojo`, which differed from it only in its
header comment.

The interval critical orbit's shared pieces are the vendored `quadratic_orbit`
package (`vendor/mojo/quadratic_orbit/`). `kernel/mojo/dynamics/interval_orbit.mojo`
imports the collision partition (`intended_pair`, `forbidden_count`) from
`quadratic_orbit/collision.mojo` and the orbit step (`zero_box`,
`quadratic_step` under the local name `next_orbit_value`), `collision_interval`
and `complex_excludes_zero` from `quadratic_orbit/orbit.mojo`; its local copies,
and the unused local `intended_count`, were removed. The two partitions agree
on every input the consumer passes: both intend nothing when `ell < 1` or
`period < 1` (so a purely periodic type, `ell = 0`, is rejected by
`OrbitEvalConfig.valid()` before partitioning and partitions to nothing if
reached anyway), and upstream additionally refuses negative indices, which no
caller passes. `excludes_zero`, the two-valued reading of
`complex_excludes_zero`, stays local. The legacy-syntax
`kernel/mojo/certificates/collision_sets.mojo` (and the other uncompiled
`fn`-era files) keeps its own partition: it is outside the compiled closure,
and its `is_intended_tail_pair` intends tail pairs at `ell = 0`, which the
upstream partition does not.

The BigZ ray address of `kernel/mojo/dynamics/bigq_ray_address.mojo` is the
vendored `rational_dynamics` `ReducedFraction`, and its doubling and equality
are `double_mod_one` and `fraction_equal`
(`vendor/mojo/rational_dynamics/rational.mojo`). `make_bigq_ray_addr` remains a
thin adapter that keeps the local contract: the input is normalized as a `Q`
first, so a negative denominator flips the sign as before, and an address
outside `[0, 1)` is refused, where upstream `reduce_fraction` would accept any
nonnegative fraction. The Int64 checked addresses of
`kernel/mojo/dynamics/checked_ray_address.mojo` stay local: upstream has no
fixed-width equivalent.

The catalogue denominator `2^l (2^k - 1)` of
`kernel/mojo/certificates/misiurewicz_catalogue.mojo` is the vendored
`angle_doubling` `type_count` (`vendor/mojo/angle_doubling/angle.mojo`): the
addresses with `2^(l+k) t = 2^l t` are exactly the multiples of that
denominator's reciprocal, and the local index and denominator bounds still
apply first. Three local readings stay, because upstream's differ:
`exact_type` reads every period up to its denominator bound `2^20`, while
upstream `period` refuses past 64 (the smoke's brute-force check reaches
`1/107`, of period 106); `angle_period` in `kernel/mojo/dynamics/angle_tuning.mojo`
reads periods of denominators up to `2^62 - 1`, while upstream `Angle` refuses
denominators past `2^30`; and `catalogue_count` counts the addresses of
*exact* type `(l, k)` by Moebius inversion, which `type_count`, counting every
address with `2^(l+k) t = 2^l t`, is not.

This changes ownership, not mathematical semantics:

- `BigZ` and `Q` remain exact, unbounded, and fail closed;
- interval predicates remain conservative and distinct from exact acceptance;
- certificate acceptance remains a consumer responsibility;
- C1 and every source-pending theorem dependency remain unresolved unless a
  separate proof record says otherwise.

The old standalone library repositories may be archived only after the PSC
consumer migration is merged and repository-wide reference checks show no
live pin to them.

