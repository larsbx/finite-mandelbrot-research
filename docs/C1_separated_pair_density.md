# C1 separated-pair density

Status: definition-level finite measure; no theorem-status change.

This note binds round-two item R3 of `docs/cross-pollination-round-two-2026-09-16.md` (N2) into the C1 program. The balanced-pair overlap route of `larsbx/pisot-substitution-conjecture-research` carries a quantitative measure of fibre collapse, the common fraction `f_m` and its limit; its parameter-space counterpart here is the measure of the pairs of external angles that a finite separator-catalogue prefix already decides. `src/C1_separated_density.mojo` computes that measure exactly over unbounded rationals.

## Terminology declaration: separated-pair density

Genealogy: The quantity is the product-measure form of the coincidence probability of a finite partition, standard in combinatorics and information theory. Its role here mirrors the common fraction `f_m` of the overlap route, and the measure it uses is Lebesgue measure on external angles, the measure the harmonic-measure literature works with.

Bridge claim: definition-only project term. The density is a finite exact computation over rational cut addresses. The identification of Lebesgue measure on angles with harmonic measure on the boundary of `M`, and the almost-everywhere triviality result that goes with it, are the scaffolded theorem tag `HarmonicMeasureAlmostEveryFibreTrivial` (`docs/C1_theorem_tag_import_ledger.md`), not a property of this computation.

Known leaks: A density approaching one would make the undecided pairs a null set, never an empty one; the infinitely renormalizable parameters of `docs/C1_residual_directive_carrier.md` lie exactly there. No finite prefix bounds the limit. The density says nothing about any named pair, and a pair that stays undecided at every prefix is the persistent non-separation frontier, not a measure statement.

Use discipline: Use only in C1 files, or with a pointer to this declaration. Never write that a density decides a pair, proves fibre triviality, or establishes local connectivity.

## Objects

A catalogue prefix contributes finitely many **two-ray separators**, each a pair of distinct rational ray addresses. A separator splits the circle of external angles into the arc between its endpoints and the complement of that arc, so it assigns every angle a side; which side is called inside is a convention that complements one bit of every signature and leaves everything below unchanged. Two parameters are separated at the prefix exactly when some separator puts them on opposite sides, that is, when their **side signatures** differ.

The endpoints cut the circle into **atoms**. Atoms sharing a signature are one undecided class `C_c`, and under the product of Lebesgue measure the decided pairs have measure

```text
density = 1 - sum_c |C_c|^2,     residue = sum_c |C_c|^2.
```

`separated_pair_density(lefts_n, lefts_d, rights_n, rights_d)` returns both, with the class and atom counts. No separator leaves the circle one atom, so the density is `0` and the residue `1`. Repetition is not refinement. The computation fails closed on a length mismatch, a malformed or out-of-range endpoint, a separator whose two rays coincide, and on atoms whose exact lengths do not sum to one, which no accepted input can produce and which is therefore a kernel self-check.

**Endpoints may not be flattened into one cut set.** Two atoms outside every separator are not separated from each other, however many separators there are, so they stay one class. With the disjoint separators `(0, 1/4)` and `(1/2, 3/4)` the four atoms fall into three classes of `1/4`, `1/2`, `1/4` and the density is `5/8`; a flat cut set would treat all four as distinct and report `3/4`, overstating the decided measure. `flattened_density` in the reference keeps that wrong quantity only as a negative control.

## Properties

- **Range.** `0 <= density <= 1 - 1/n` for `n` signature classes, with equality exactly for classes of equal measure.
- **Refinement monotonicity.** Adding a separator refines the signature partition, so it never lowers the density.
- **Orientation independence.** Exchanging a separator's two endpoints leaves the density and the class measures unchanged.
- **Exactness.** Every length, midpoint, square, and sum is an unbounded rational; no floating point appears, as `docs/rational-interval-arithmetic-spec.md` requires of certificate-relevant numbers.

Pinned instances, asserted identically by the Mojo smoke target and by `tools/separated_density_reference.py`:

| Separators | Classes | Density |
| --- | --- | --- |
| `(1/3, 2/3)` | `1/3, 2/3` | `4/9` |
| `(2/3, 1/3)` | the same, reversed | `4/9` |
| `(0, 1/4)` and `(1/2, 3/4)` | `1/4, 1/2, 1/4` | `5/8` |
| `(1/7, 2/7)` and `(2/7, 4/7)` | `1/7, 2/7, 4/7` | `4/7` |
| `(1/3, 2/3)` and `(0, 1/3)` | three thirds | `2/3` |
| `(1/3, 2/3)` twice | `1/3, 2/3` | `4/9` |
| none | one class | `0` |

## Non-claims

`density_one_implies_every_pair_separated()`, `finite_prefix_density_decides_persistent_non_separation()`, and `density_is_harmonic_measure_of_the_boundary()` all return `False`. The correct form of the imported statement is

```text
PersistentNonSeparation(A,B) and A != B  =>  A, B lie in a harmonic-measure-null class
```

with the null class named, which is what the theorem tag records and what its `exceptional_set_is_null_not_empty` payload field forces a user to state. C1 remains an open frontier.

## Next step

Attach a density to each level of a carrier's catalogue prefix, so that a refinement step reports the measure it decided as well as the addresses it added, and record whether the residue is non-increasing along the C1 carrier-refinement order.
