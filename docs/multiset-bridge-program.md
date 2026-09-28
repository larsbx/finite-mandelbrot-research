# Multiset bridge program

**Status:** staged theorem program. The algebraic identities in stages B0 and
B1, the simple-residue-root subcertificate, one replayable Hensel step from
modulo `p` to modulo `p^2` are executable in
`kernel/mojo/dynamics/critical_relation_bridge.mojo`, together with bounded factor provenance
for monic linear factors. The rational `c = -2` subcase now also has an
executable B3 root-handle replay into the dyadic localization calculus. The
unbounded lift, general factor correspondence, and later stages require the
stated certificates or imported theorems. This program keeps
multisets in the primary research toolbox without identifying an arbitrary
finite-field statistic with the classical Mandelbrot set.

## Objective

Construct explicit bridges from multiplicity-bearing finite objects to
characteristic-zero parameter information for

```text
f_c(z) = z^2 + c,
Q_0(C) = 0,
Q_{n+1}(C) = Q_n(C)^2 + C.
```

The word `multiset` is an interface. Every instance must declare what its
coefficient counts. Different coefficient semantics support different bridges.

## Bridge ladder

### B0 — Common integral recurrence

Each `Q_n` lies in `Z[C]`. Therefore formation of the critical-orbit sequence
commutes exactly with reduction modulo every prime:

```text
reduce_p(Q_n)(c_bar) = f_bar_c^n(0).
```

This is an equality of finite algebraic computations, not an asymptotic
analogy.

### B1 — Critical-relation divisors

For `ell >= 0` and `k >= 1`, define

```text
A_{ell,k}(C) = Q_{ell+k}(C) - Q_ell(C).
```

The effective root divisor

```text
R_{ell,k} = div_0(A_{ell,k})
```

is a multiset: each parameter root is counted with its algebraic multiplicity.
Its reduction modulo `p` is computed by reducing the same integral polynomial.
This gives a canonical finite multiset with a direct characteristic-zero
ancestor.

`A_{ell,k}(c) = 0` proves only a return relation. Exact preperiod and period
require exclusions of every earlier or unintended collision. The repository's
existing intended/forbidden collision partition is the required starting
certificate.

The first multiplicity calculation is now executable. For
`A_{2,1}(C)=C^3(C+2)`, repeated exact division gives

```text
div_0(A_{2,1}) = 3[0] + [-2].
```

Filtering by the minimal collision pattern removes `C=0`, whose critical
orbit already has type `(0,1)`, and retains `C=-2` with exact type `(2,1)`:

```text
D^{exact}_{2,1} = [-2].
```

Thus root multiplicity is not exact-type multiplicity. The executable
`CriticalRelationDivisorMultiset` records both cycles and checks that the raw
multiplicities sum to the degree before applying the exact-type filter.

The next relation demonstrates where the rational subcase stops. Exact
factorization gives

```text
A_{4,1}(C) =
  C^5(C+2)(C^3+2C^2+2C+2)F_7(C),
deg(F_7)=7.
```

Repeated exact division removes the known lower-type contribution
`5[0]+[-2]` and produces a degree-10 residual candidate divisor

```text
div_0((C^3+2C^2+2C+2)F_7(C)).
```

The executable `R41ResidualDivisorMultiset` checks the factorization and
degree accounting. The follow-on `R41AlgebraicRootCertificate` uses exact
Euclidean gcd calculations after reduction modulo 5. It verifies that both
non-rational factors are squarefree and coprime, that the cubic factor divides
the earlier collision `Q_4-Q_3`, and that `F_7` is coprime to every
unintended collision through the required horizon. Thus the cubic is a
lower-type contribution, while

```text
D^{exact}_{4,1} = div_0(F_7)
```

has seven distinct algebraic roots of exact critical-orbit type `(4,1)`.
This is an algebraic factor and collision certificate. It does not choose or
localize any embedding, so it supplies no B3 root handle and makes no density,
equidistribution, or C1 claim.

### B2 — Good-reduction and lifting certificate

A residue-class root may be used in the bridge only with a certificate that
records:

1. `A_{ell,k}(c_bar) = 0` modulo `p`;
2. the derivative is nonzero modulo `p`, or a separately verified
   multiplicity treatment;
3. all exact-type collision exclusions;
4. the relevant discriminant and resultant nonvanishing conditions;
5. a factor/root correspondence or Hensel lift.

For a simple residue root, Hensel lifting supplies a unique root in the chosen
`p`-adic residue class. Because it satisfies the same integral
critical-relation polynomial, its algebraic conjugates in characteristic zero
are postcritically finite parameters after the exact-type exclusions are
verified. Their critical orbits are finite, hence bounded, so their complex
embeddings lie in the classical Mandelbrot set.

This stage bridges a certified root multiset to a postcritically finite
submultiset of `M`; it does not bridge every finite-field parameter to `M`.

Current executable boundary: the checker verifies bounded primality,
commutation of polynomial reduction with direct iteration, the minimal-horizon
exact collision pattern, and a nonzero modular derivative. From an accepted
simple root it computes the unique correction digit and verifies the compatible
root modulo `p^2`. This is a finite Hensel step, not an asserted infinite
`p`-adic lift. The checker does not yet produce a characteristic-zero factor
correspondence, complex embedding, localization, or discriminant/resultant
evidence.

The first characteristic-zero factor subcase is also executable: for a bounded
integer root, the checker replays synthetic division by `C - r`, exact
recomposition, simple-root differentiation, and agreement of `r` with the
certified residues modulo `p` and `p^2`. This proves factor provenance for
rational PCF parameters such as `c = -2`. It is not a general factorization
algorithm and says nothing yet about non-rational complex embeddings.

### B3 — Localization into the existing certificate calculus

For a selected complex embedding, the bridge must construct the existing
finite root handle:

```text
(squarefree factor, dyadic localization box, uniqueness witness).
```

The output can then use the ordinary landing, ray-address, and theorem-tag
interfaces. The finite-field record is provenance for the candidate and its
multiplicity; the characteristic-zero localization is what admits it to the
classical certificate layer.

The first executable B3 subcase is `RationalB3RootHandle` in
`kernel/mojo/dynamics/multiset_b3_localization.mojo`. For `c = -2`, it composes:

1. the modular simple-root and one-step Hensel provenance at `p = 5`;
2. exact characteristic-zero factor provenance for `C + 2`;
3. the dyadic box for `P_{2,1}=C(C+2)`;
4. the exact Krawczyk contraction proving a unique root in that box; and
5. direct integer replay of the critical orbit `0,-2,2,2`.

The rational root has a canonical characteristic-zero embedding, but the
current BigZ/Q backend is still designated non-proof-grade. Accordingly,
`arithmetic_replay_accepted()` records the successful finite composition while
`accepted()` and `proof_grade_accepted()` remain false until the repository
proof-backend gate opens. This does not yet close the acceptance-bearing B3
handoff. General algebraic factors, conjugate selection, and non-rational
complex embeddings remain fail-closed.

### B4 — Distributional bridge

Postcritically finite parameter divisors are not merely isolated examples.
Published equidistribution results provide a route in which normalized
postcritically finite parameter multisets converge to the bifurcation measure
in polynomial parameter spaces. In the quadratic family this is the measure
supported on the Mandelbrot bifurcation locus.

The repository must pin the precise family, normalization, allowed
combinatorics, exceptional sets, and convergence mode before importing this as
a theorem tag. Relevant primary sources include:

- Charles Favre and Thomas Gauthier, *Distribution of postcritically finite
  polynomials*, arXiv:1302.0810;
- Thomas Gauthier and Gabriel Vigny, *Distribution of postcritically finite
  polynomials II: Speed of convergence*, arXiv:1505.07325;
- Thomas Gauthier and Gabriel Vigny, *Distribution of postcritically finite
  polynomials III: Combinatorial continuity*, arXiv:1602.00925.

B4 is the proposed global bridge from a sequence of algebraic multisets to a
canonical measure on the classical boundary. It is not yet an imported theorem
in the project ledger.

## Coefficient-semantics matrix

| Multiset coefficient | Immediate bridge | Missing obligation |
|---|---|---|
| algebraic root multiplicity of `A_{ell,k}` | B0–B3 | good reduction, exact type, localization |
| exact-type witness count | B1–B3 after quotienting duplicate encodings | canonical witness equivalence |
| Frobenius-orbit multiplicity | arithmetic descent data | embedding and lift certificate |
| critical-basin cardinality over `F_p` | finite functional-graph invariant only | comparison theorem to a critical-relation divisor or height |
| projective intersection multiplicity at infinity | divisor-theoretic escape data | relation to the marked critical section |
| certified dyadic escape-witness count | subset of the classical complement | coverage and overlap normalization |

The basin multiset introduced in `kernel/mojo/dynamics/projective_multiset.mojo` therefore
remains in the toolbox. It is not discarded; it occupies a different bridge
column from algebraic root multiplicity.

## First implementable theorem target

For fixed bounded `(ell,k,p)`, produce a replayable record containing:

```text
A_{ell,k} over Z
its reduction modulo p
the residue root and derivative
all forbidden-collision evaluations
the squarefree characteristic-zero factor
a dyadic localization witness for one complex embedding
the equality between declared multiplicity and the factor/root calculation
```

Acceptance proves that the localized characteristic-zero parameter has the
declared exact critical-orbit type and lies in `M`. It makes no density,
boundary-coverage, or MLC claim.

## Non-claims

- Large finite-field basin weight does not presently imply proximity to the
  classical boundary.
- Reduction modulo one prime does not recover a complex parameter uniquely.
- Hensel lifting alone does not choose a complex embedding or localization.
- Equidistribution does not imply setwise convergence, local connectivity, or
  that any finite level covers the boundary.
