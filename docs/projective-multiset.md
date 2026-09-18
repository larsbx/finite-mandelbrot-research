# Projective multisets and the infinity divisor

**Status:** exact finite-field definition and implementation contract. This
document proves no claim about Mandelbrot local connectivity and does not
identify a finite-field shadow with the classical Mandelbrot set.

## Projective quadratic morphism

For a field `K` and parameter `c`, the polynomial recurrence `z |-> z^2 + c`
extends to the morphism

```text
F_c [X:Z] = [X^2 + c Z^2 : Z^2]
```

on the projective line. The projective class `infinity = [1:0]` is fixed. Its
pullback divisor is

```text
F_c^* [infinity] = 2 [infinity],
(F_c^n)^* [infinity] = 2^n [infinity].
```

This is an exact algebraic statement: infinity is totally ramified. In the
local parameter `w = Z/X`, the transformed coordinate is

```text
w |-> w^2 / (1 + c w^2),
```

so its vanishing order at `w = 0` doubles. This is the projective algebraic
content behind attraction to infinity; it requires no circle, transcendental
function, metric limit, or analytic complex-number primitive.

For finite `c` the affine chart is invariant. Consequently, an affine orbit
over `F_q` never lands on the infinity divisor, even though the divisor and
its ramification are algebraically meaningful. The following statements must
therefore remain distinct:

1. affine landing at infinity, which does not occur here;
2. intersection multiplicity with the infinity divisor in a projective
   closure;
3. pullback multiplicity of the invariant infinity divisor;
4. pole-order growth at a valuation over a function or global field.

Only items 1 and 3 are implemented in the first finite-field slice.

## Effective zero-cycles

A finite projective multiset is represented mathematically as an effective
zero-cycle

```text
D = sum_v m_v [v],     m_v in N.
```

Its support is the set of projective classes with nonzero coefficient. A
coefficient must always declare its semantics. Basin cardinality, witness
count, polynomial-root multiplicity, intersection multiplicity, and
extension-field fibre cardinality are different invariants and are not
interchangeable.

The first executable coefficient is the **critical-basin multiplicity**

```text
b_p(c) = #{z in F_p : the eventual cycle of z equals the critical cycle}.
```

It is graded by the exact critical-orbit signature `(tail, period)`. Hence the
finite parameter zero-cycle is

```text
D_p = sum_{c in F_p} b_p(c) [c:1]_(tail(c), period(c)).
```

This enriches finite functional-graph statistics without changing the
existing Mandelbrot-support or certificate definitions.

## Extension fields

Over extensions, a zero-cycle defined over `F_q` may contain a full Frobenius
orbit of projective classes even when its individual classes are not rational
over `F_q`. A later extension-field implementation must therefore encode
Frobenius-stable cycles, not merely lists of `F_q`-rational classes.

## Claim firewall

The following do not follow from the implemented multiset:

- an escape classification of the classical parameter plane;
- a finite-field replacement for the classical Mandelbrot set;
- local connectivity, fibre triviality, or landing of external rays;
- an analytic basin measure;
- a theorem transferring a finite-field multiplicity distribution to
  characteristic zero.

Any such bridge requires its own theorem tag, hypotheses, and source record.

## Executable contract

`src/projective_multiset.mojo` provides:

- exact critical tail and period over a caller-supplied prime field;
- exact critical-basin cardinality;
- one graded effective-zero-cycle coefficient per parameter;
- the bounded exact identity `mult_infinity((F_c^n)^*[infinity]) = 2^n`;
- fail-closed rejection outside the fixed-width multiplicity bound;
- the theorem-level invariant that affine polynomial orbits do not land on
  the infinity divisor.

The module currently treats primality as an explicit caller precondition and
rejects moduli above its declared fixed-width execution bound. Supporting
general prime powers requires a finite-field representation and is not
silently approximated by arithmetic modulo a composite integer.
