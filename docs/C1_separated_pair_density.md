# C1 separated-pair density

Status: definition-level finite measure; no theorem-status change.

This note binds round-two item R3 of `docs/cross-pollination-round-two-2026-09-16.md` (N2) into the C1 program. The balanced-pair overlap route of `larsbx/pisot-substitution-conjecture-research` carries a quantitative measure of fibre collapse, the common fraction `f_m` and its limit; its parameter-space counterpart here is the measure of the pairs of external angles that a finite separator-catalogue prefix already decides. `src/C1_separated_density.mojo` computes that measure exactly over unbounded rationals.

## Terminology declaration: separated-pair density

Genealogy: The quantity is the product-measure form of the coincidence probability of a finite partition, standard in combinatorics and information theory. Its role here mirrors the common fraction `f_m` of the overlap route, and the measure it uses is Lebesgue measure on external angles, the measure the harmonic-measure literature works with.

Bridge claim: definition-only project term. The density is a finite exact computation over rational cut addresses. The identification of Lebesgue measure on angles with harmonic measure on the boundary of `M`, and the almost-everywhere triviality result that goes with it, are the scaffolded theorem tag `HarmonicMeasureAlmostEveryFibreTrivial` (`docs/C1_theorem_tag_import_ledger.md`), not a property of this computation.

Known leaks: A density approaching one would make the undecided pairs a null set, never an empty one; the infinitely renormalizable parameters of `docs/C1_residual_directive_carrier.md` lie exactly there. No finite prefix bounds the limit. The density says nothing about any named pair, and a pair that stays undecided at every prefix is the persistent non-separation frontier, not a measure statement.

Use discipline: Use only in C1 files, or with a pointer to this declaration. Never write that a density decides a pair, proves fibre triviality, or establishes local connectivity.

## Objects

A catalogue prefix contributes finitely many rational ray addresses, its **cuts**. The distinct cuts, taken in cyclic order, split the circle of external angles into arcs `I_1, ..., I_n` with exact rational lengths summing to one. Two parameters whose angles lie in different arcs are separated at that prefix, so under the product of Lebesgue measure the decided pairs have measure

```text
density = 1 - sum_j |I_j|^2 = sum_{i != j} |I_i| |I_j|,     residue = sum_j |I_j|^2.
```

`separated_pair_density(nums, dens)` returns both, with the number of arcs. Fewer than two distinct cuts leave the circle a single arc, so the density is `0` and the residue `1`: one ray is not a separation. Repetition is not refinement; duplicate addresses collapse. The computation fails closed on a length mismatch, a malformed or out-of-range address, and on arcs whose exact lengths do not sum to one, which no accepted input can produce and which is therefore a kernel self-check.

## Properties

- **Range.** `0 <= density <= 1 - 1/n` for `n` arcs, with equality exactly for `n` arcs of equal length.
- **Refinement monotonicity.** Adding a cut never lowers the density. The reference checks this exhaustively over every subset of the twelfth roots of size at most six.
- **Exactness.** Every length, square, and sum is an unbounded rational; no floating point appears, as `docs/rational-interval-arithmetic-spec.md` requires of certificate-relevant numbers.

Pinned instances, asserted identically by the Mojo smoke target and by `tools/separated_density_reference.py`:

| Cuts | Arcs | Density |
| --- | --- | --- |
| `1/3, 2/3` | `1/3, 2/3` | `4/9` |
| `1/7, 2/7, 4/7` | `1/7, 2/7, 4/7` | `4/7` |
| `0, 1/3, 2/3` | three thirds | `2/3` |
| `1/3, 2/3, 1/3` | as `1/3, 2/3` | `4/9` |
| `1/3` or none | one arc | `0` |

## Non-claims

`density_one_implies_every_pair_separated()`, `finite_prefix_density_decides_persistent_non_separation()`, and `density_is_harmonic_measure_of_the_boundary()` all return `False`. The correct form of the imported statement is

```text
PersistentNonSeparation(A,B) and A != B  =>  A, B lie in a harmonic-measure-null class
```

with the null class named, which is what the theorem tag records and what its `exceptional_set_is_null_not_empty` payload field forces a user to state. C1 remains an open frontier.

## Next step

Attach a density to each level of a carrier's catalogue prefix, so that a refinement step reports the measure it decided as well as the addresses it added, and record whether the residue is non-increasing along the C1 carrier-refinement order.
