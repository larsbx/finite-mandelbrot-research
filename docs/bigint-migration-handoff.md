# BigInt Migration Handoff

## Purpose

The repository retains bounded `Int64` transition/demo paths for negative controls, but the canonical exact rational path now uses the dynamic-limb BigZ backend and normalized BigZ-backed `Q`. Full proof-grade certificate acceptance remains fail-closed until every acceptance-bearing downstream predicate and imported theorem obligation is discharged.

## Non-negotiable invariant

Do not change the certificate semantics to fit the backend.

The backend must satisfy the calculus, not the other way around.

## Required integer backend properties

A certificate-ready backend must provide:

1. unbounded signed integers;
2. exact addition, subtraction, multiplication, and negation;
3. exact order comparison;
4. Euclidean gcd;
5. exact divisibility with rejected non-divisions;
6. deterministic canonical serialization;
7. an explicit `allows_certificate_acceptance=true` gate.

## Required rational backend properties

`Q` must become a normalized fraction over the bigint backend:

```text
Q = num / den
where den > 0 and gcd(abs(num), den) = 1
```

Every constructor and operation must normalize. Equality and order may use cross multiplication only after the bigint backend is active.

## Files that define the gate

- `src/bigint_adapter.mojo`
- `src/rat_backend_plan.mojo`
- `src/cert_backend.mojo`
- `src/proof_grade_gate.mojo`
- `tests/test_backend_migration.py`
- `tests/test_proof_grade_gate.py`

## Migration sequence

0. Use `src/checked_int64_backend.mojo` to fail closed during migration. Its
   compiled Q_8 growth control confirms the present bounded backend cannot
   complete the intended recurrence. This layer does not itself permit
   certificate acceptance and `Q` has not yet been migrated to it.
   `src/checked_q.mojo` now supplies the normalized, rejection-aware rational
   API over that transition layer. `src/checked_interval_q.mojo` now propagates
   rejection through the real rational-interval operations.
   `src/checked_complex_interval.mojo` now carries rejection through rank-2
   interval arithmetic and `P_{2,1}` Horner evaluation.
   `src/checked_krawczyk_witness.mojo` now propagates rejection through strict
   inclusion and the complete `P_{2,1}` contraction calculation. The next slice
   `src/checked_interval_exclusion.mojo` now computes all five forbidden
   `P_{2,1}` orbit collisions on the same checked c=-2 box and fails closed on
   arithmetic rejection or ambiguous zero containment.
   `src/certificate_arithmetic_migration_gate.mojo` separates checked-width
   localization acceptance from proof-grade acceptance and binds the checked
   contraction to that computed exact-type result on the same box. The next
   slice inventories the remaining downstream predicates in
   `docs/certificate-predicate-migration-inventory.md`.
   `src/checked_ray_address.mojo` computes the c=-2 rational ray orbit with
   fixed-width overflow rejection, and `src/checked_finite_certificate_gate.mojo`
   now proves that checked finite inputs are insufficient for proof-grade use.
   `src/checked_landing_target_adapter.mojo` retains the bounded-width `1/2`
   to c=-2 association as a migration cross-check. The acceptance-bearing
   successor `src/proof_grade_landing_target_association.mojo` now identifies
   the target with exact BigZ/Q ray replay, exact BigZ replay of
   `R_{2,1}=C^3(C+2)`, lower-type exclusion of `C=0`, exact type-`(2,1)`
   verification at `C=-2`, and the canonical checked rational-ray theorem
   import record. The rational landing import is therefore admissible without
   using the checked-width localization gate. The Misiurewicz trivial-fiber
   classification remains fail-closed.
1. **Selected:** Mojo-native dynamic base-`10^9` limbs in `src/finite_exact/bigint_z.mojo`.
2. **Complete:** the integer layer implements unbounded signed storage, exact
   add/sub/mul/order, quotient/remainder, rejected non-divisions, Euclidean gcd,
   and canonical `Z(sign, byte_len, big_endian_magnitude)` serialization.
3. **Complete:** `Q` stores normalized `BigZ` numerator and denominator values while preserving its public arithmetic names; invalid denominators and division by zero propagate rejection.
4. **Complete (arithmetic hardening):** the public boundary of `BigZ`, `Q`, `IQ`, and `ComplexIQ` is declared in `docs/exact-arithmetic-public-boundary.md`; long division replaces shift-and-subtract; `Q` cancels before multiplying and comparing; the randomized property probe runs against the Python oracle in CI.
5. **Complete for the c=-2 replay path:** interval arithmetic, exact-type
   exclusions, rational ray-address replay, and the proof-grade landing-target
   association now execute on the BigZ/Q path.
6. **Next theorem boundary:** validate the class-specific Misiurewicz
   trivial-fiber import for the exact type-`(2,1)` `c=-2` instance.
7. Keep complete certificate acceptance fail-closed until that theorem import,
   incidence serialization/replay requirements, and every remaining
   acceptance-bearing gate are satisfied.

## Forbidden shortcuts

Do not use:

- bounded integer overflow assumptions;
- floating approximations;
- analytic trigonometry;
- analytic point membership;
- lower-factor gcd stripping for exact type.

The accepted pipeline remains:

```text
squarefree localization
+ same-box forbidden collision exclusions
+ rational ray-address combinatorics
+ theorem tags
+ PointVertex incidence packaging
+ proof-grade bigint/rational backend
```
