# The atlas dataset: every exact object, printed once

**Scope.** An engineering change. No mathematical claim changes and no verdict
moves: `src/atlas_dataset.mojo` asks each module for the answer it already
computes and prints it as JSON. It is the boundary where the exact objects
leave this repository, and it holds the policy at that boundary.

## 1. Why a single emitter

The exact objects were reachable only by running a module's smoke case or by
re-implementing the pipeline outside Mojo. Anything that wanted to *show* them
— a page, a note, a reviewer's spreadsheet — reached for the Python references
in `tools/`, which are oracles, not the canonical implementation. That inverts
the repository's own policy: Mojo owns the executable research once a Mojo
module exists.

`pixi run atlas-dataset` prints all of it in one run:

| Section | Module asked |
| --- | --- |
| `counts`, `catalogues` | `misiurewicz_catalogue` |
| `kneading` | `C1_residual_directive_carrier` |
| `tunings` | `angle_tuning` |
| `graphs` | `C1_misiurewicz_prefix_graph` |
| `density` | `C1_separated_density` |
| `incidence` | `bigq_certificate_incidence` and the gate beneath it |

## 2. What is not in it

Positions in the parameter plane. They are floating point, no module under
`src/` may produce one, and `tools/audit_exact_arithmetic.py` enforces that.
A consumer that wants to draw the objects computes positions itself and says
so; `tests/test_atlas_dataset.py` fails if a float ever reaches a section.

The catalogue still locates nothing. What the repository does locate is a
*box*, and the incidence section carries exactly what that means.

## 3. Three changes the emitter needed

**The extractor reports its pairs.** `PrefixExtraction` counted nonproductive
pairs and sink cycles without naming them, so a reader could not see the
obstruction, only its size. It now carries `nonproductive_codes` and
`cycle_codes`, filled in the same pass the counts come from — no second run of
the pipeline, and no way for the two to disagree. A pair is one Int, as
`_code` packs it, so a reader decodes `(code // den, code % den)`.

**The internal address is a list.** `_internal_address_contains` walked the
address without ever building it. `internal_address(nu)` returns it, and the
membership test reads that list, so the address shown and the address tested
are the same object. The basilica is 1 → 2, the rabbit 1 → 3, the airplane
1 → 2 → 3.

**Exact numbers can be read in base ten.** `src/exact_decimal.mojo` renders a
`BigZ` and a `Q` as decimal digits. Limbs are base `10^9`, so this is
concatenation, not division: no rounding, no floating point, and a rejected `Q`
renders as `rejected` rather than as a number. It sits outside `finite_exact/`
because that package is vendored byte for byte from `larsbx/finite-math-kernels`
and its digests are checked; a renderer is a consumer of the kernel's public
accessors, not part of the kernel. Binding row in
`docs/rational-interval-arithmetic-spec.md` section 6.2.

## 4. Verification

- `tests/test_atlas_dataset.py` runs the emitter and checks every section
  against the independent Python oracles: counts and catalogues, kneading
  sequences with their internal addresses and twists, tuned angles, the
  extractions **down to the individual nonproductive pairs and cycle
  members**, and the exact densities. The pinned extraction is still the pinned
  one: type (1, 3) over denominator 14 gives 12 vertices, 37 undecided, 20
  nonproductive, 2 merging, 2 boundary cycles, 0 interior, and is not
  obstruction free.
- The non-claims are asserted on the output, not just in the source: at every
  box half-width the package is valid and the certificate is still **not**
  emitted, the theorem import is **not** accepted, and `proves_c1` is false.
- The Mojo smoke suite carries the three additions as named cases and stays at
  59 cases, all passing.
