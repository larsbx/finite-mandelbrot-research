# C1 Misiurewicz exact-type catalogue

Status: definition-level finite catalogue with an exact counting regression; no theorem-status change.

This note discharges round-one item B6 of `docs/cross-pollination-round-two-2026-09-16.md`, recorded there as "the rationale was corrected, the catalogue object and the angle-count regression were not built". It supplies both. It is also the prerequisite the round-two document names for item R5, the obstruction extractor on Misiurewicz prefix graphs: that item needs a finite set of addresses per exact type before an extractor has anything to run on.

## Terminology declaration: exact-type catalogue

Genealogy: Misiurewicz parameters and their exact preperiod and period are standard in complex dynamics, and the reading of both off the denominator of a rational external angle is the standard symbolic fact about doubling. The catalogue is the finite set of those addresses for one type; the word carries no new mathematics.

Bridge claim: definition-only project term. The catalogue holds ray addresses, which are finite symbolic objects, not parameters and not points. Associating a parameter with an address needs a landing tag and an adapter; triviality of the corresponding fibres is the imported tag `KnownTrivialFiberClass` under its own hypotheses.

Known leaks: A catalogue is finite by construction and bounded by `MAX_CATALOGUE_DENOMINATOR`; it is not a statement about all types, and an exhausted small type says nothing about a larger one. The counting identity is exact arithmetic, not evidence about the parameter plane.

Use discipline: Use in C1 files or with a pointer to this declaration, and only for sets of addresses. A catalogue does not locate a parameter, decide a fibre, or settle C1, and must not be written as if it did.

## Exact type

For a ray address `p/q` in lowest terms, write `q = 2^l m` with `m` odd. Under doubling modulo one the address has preperiod `l` and period the multiplicative order of `2` modulo `m`, with `m = 1` giving period one because zero is fixed. The address is of **Misiurewicz type** when `l >= 1`, that is, when the orbit is strictly preperiodic; `1/3` has preperiod zero and is periodic, so it is not, while `1/2` and `1/6` are.

`exact_type(num, den)` returns both indices and refuses an address outside `[0, 1)`, a non-positive denominator, and a denominator beyond the bound. Reduction happens first, so `2/6` is read as `1/3`.

## The catalogue and its counting identity

Every address of exact type `(l, k)` is `p / (2^l m)` in lowest terms with `m` odd of multiplicative order `k`, and every such `m` divides `2^k - 1`. The addresses therefore share the denominator

```text
catalogue_denominator(l, k) = 2^l (2^k - 1),
```

and counting them gives, since there are `phi(2^l m) = 2^(l-1) phi(m)` numerators for each `m` and the orders sum by Moebius inversion over the divisors of `2^k - 1`,

```text
count(l, k) = 2^(l-1) * sum_{d | k} mu(k/d) (2^d - 1).
```

`catalogue(l, k)` enumerates the numerators and `catalogue_matches_count(l, k)` compares the enumeration with the identity. That comparison is the round-one angle-count regression: the Mojo smoke target runs it for every type with `1 <= l, k <= 4`, and `tools/misiurewicz_catalogue_reference.py` for every type with `1 <= l, k <= 7`, forty-nine in all.

Pinned catalogues, asserted identically on both sides:

| Type `(l, k)` | Denominator | Addresses | Count |
| --- | --- | --- | --- |
| `(1, 1)` | `2` | `1/2` | `1` |
| `(2, 1)` | `4` | `1/4, 3/4` | `2` |
| `(1, 2)` | `6` | `1/6, 5/6` | `2` |
| `(1, 3)` | `14` | `1/14, 3/14, 5/14, 9/14, 11/14, 13/14` | `6` |
| `(2, 3)` | `28` | twelve addresses | `12` |
| `(3, 3)` | `56` | twenty-four addresses | `24` |

## Bounds and fail-closed behaviour

Types are refused beyond `MAX_TYPE_INDEX` and denominators beyond `MAX_CATALOGUE_DENOMINATOR`, before any arithmetic, so no computation here can overflow its fixed-width integers; `catalogue_denominator` returns `-1` and `catalogue` the empty list. A bound reached is a refusal, never an answer.

## Non-claims

`catalogue_is_a_set_of_parameters()` and `catalogue_proves_fibre_triviality()` return `False`. The catalogue is a finite set of symbolic addresses. It locates nothing, and the triviality of the fibres of Misiurewicz parameters remains the imported theorem tag with its stated hypotheses.

## Next step

Round-two item R5: pair a catalogue's addresses into two-ray separators, measure the prefix with `docs/C1_separated_pair_density.md`, and run the obstruction extractor of `docs/C1_F1_obstruction_extraction.md` on the resulting finite graph, where the imported triviality tag predicts an empty obstruction and so supplies the first executable negative control of the kind the Pisot program uses.
