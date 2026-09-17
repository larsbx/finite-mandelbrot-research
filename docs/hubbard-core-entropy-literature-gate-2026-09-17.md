# Literature gate — a census of the algebraic type of core entropy

## Proposed step

Round-one item B8, carried into round-two item R7, proposes:

> For a postcritically finite quadratic parameter, the Hubbard tree map is Markov
> on edges and its transition matrix `A_c` is a non-negative integer matrix with
> `rho(A_c) = exp(h_core(c))`. Deliverable: for all Misiurewicz parameters with
> `(l, k)` in a box, the exact algebraic type of `exp(h_core)` — Pisot, Salem, or
> other Perron — and for the Pisot cases the balanced-pair algorithm run on the
> induced edge substitution.

B8's own text set the condition this note discharges: *"Whether 'Pisot core
entropy' has been characterized in the literature must be searched before any
claim."* It also recorded the blocker, that the Pisot test was cubic-only. That
blocker is gone: the degree-`n` screen merged as `PSC: 31effdb`.

This review asks whether the census is already answered, which hypotheses
transfer, which families break it, and where the code can actually live.

## Decision

**Proceed, with the target narrowed to the fiber question and the primitive
subfamily, and with two claims withheld.**

The census is not foreclosed. Thurston characterised which numbers arise; he did
not answer which parameters give which, and that second question is the one B8
asks. But three things have to be fixed before any code is written: the census
must partition by primitivity rather than assume it, it must not present itself
as computing the Thurston set or the Master Teapot, and it needs the screen to
be reachable, which today it is not.

## Findings

### 1. The image set is characterised. The fiber is not, and that is the census

Thurston's theorem settles which numbers occur: a positive real `h` is the
topological entropy of a postcritically finite self-map of the interval if and
only if `exp(h)` is a **weak Perron number**, that is a real positive algebraic
integer at least as large as the modulus of each of its Galois conjugates.[^1]
[^2] So "which algebraic numbers are core entropies" is answered, and a census
that framed itself as discovering that would be rediscovering a known theorem.

What is not answered is the assignment. The survey literature states the open
direction in as many words: describing the shape of the Master Teapot or the
Thurston set is *a step toward characterising which weak Perron numbers arise as
the growth rates of which* postcritically finite interval maps.[^3] That is the
fiber of Thurston's map, and B8's census — fix a box of Misiurewicz types
`(l, k)`, report the algebraic type of each `exp(h_core)` — is a finite sample of
exactly it.

Searching for a characterisation of *Pisot* core entropy specifically returned
none. That is weak evidence and is recorded as such: it means no such result
surfaced, not that none exists. Any write-up must repeat the search against a
mathematician's reading rather than rely on this note.

### 2. The growth rate is confined to `[1, 2]`, which makes the target set small and largely known

For a quadratic Hubbard tree the transition matrix has a strong constraint.
Because `f_c : T_c -> T_c` is surjective and at most two-to-one, every row of `A`
sums to `1` or `2`, so

```text
1 <= lambda <= 2,        lambda = rho(A_c) = exp(h_core(c)).
```

This is stated and used directly in the core-entropy literature.[^4] It is the
single most useful fact for scoping the census, because the Pisot numbers in
that window are unusually well understood:

- the smallest Pisot number is the plastic constant `1.3247...`, the real root of
  `z^3 - z - 1`, identified by Salem and proved minimal by Siegel, both 1944;[^5]
- the set of Pisot numbers is closed, also Salem 1944, and its smallest limit
  point is the golden ratio `1.6180...`;[^5]
- every Pisot number below the golden ratio is known explicitly, by Dufresnoy
  and Pisot 1955.[^5]

So a census reporting "Pisot" is reporting membership in a set that is, in the
relevant range, enumerable. That is a reason to be *more* careful rather than
less: a hit is checkable against a known list, so a hit that is not on the list
is a bug in the census before it is a discovery.

At the top of the range `lambda = 2` occurs, at `c = -2`. Two is a rational
integer and therefore trivially Pisot, and reporting it as an interesting Pisot
case would be an artefact.

### 3. Perron–Frobenius transfers, and its failure set is named exactly

The census wants to feed `A_c` to the repository's existing exact screens. Those
screens carry hypotheses: `is_pip` requires a **primitive** matrix with an
**irreducible** characteristic polynomial, and the degree-`n` screen decides root
location only, refusing irreducibility above degree three.

The failure set is not vague. `A` is reducible or imprimitive precisely when
`f_c` is simply or crossed renormalizable with `c-hat != 0`, or `c` is an
immediate satellite centre; and for beta-type Misiurewicz points `A` is
irreducible and primitive.[^4] Two consequences:

- The census must **partition** its box by that condition and report the classes
  separately. Filtering the awkward parameters out silently would turn a
  hypothesis into a selection effect, and the beta-type family is the clean
  subfamily where the screen applies as written.
- In the imprimitive case the characteristic polynomial factors as
  `x^k P(x^p)`.[^4] An irreducibility test on the raw characteristic polynomial
  will therefore correctly answer "reducible", and that answer must **not** be
  recorded as "not Pisot". It is a statement about the matrix's periodicity, not
  about the arithmetic of `lambda`. The screen already separates root location
  from irreducibility and refuses rather than guessing; the census has to respect
  that separation at the reporting layer too.

### 4. The Master Teapot is a different object, and the census must not claim it

The Thurston set and the Master Teapot are built from the **closure of the set of
Galois conjugates** of growth rates.[^3] [^6] The census asks, for one parameter
at a time, whether every conjugate of `lambda` lies strictly inside the unit
circle. Those are related — both concern conjugates against the unit circle, and
the Teapot literature studies exactly the persistence of roots inside it — but
they are not the same question, and one does not compute the other.

A finite census of individual parameters is a sample of the fiber. It is not an
approximation to a closure, and a picture produced from it is not a Teapot. This
note records the distinction in advance because it is the obvious way for the
write-up to overclaim.

### 5. Negative controls the census must carry

| Control | Case | What it catches |
| --- | --- | --- |
| Core entropy zero | `h = 0`, so `lambda = 1` | a Pisot number is `> 1`, so these are outside the question, not negative answers to it[^7] |
| The Chebyshev endpoint | `c = -2`, `lambda = 2` | a rational integer is trivially Pisot; reporting it as a find is an artefact |
| Satellite and renormalizable | `A` reducible or imprimitive | the screen's hypotheses fail; `x^k P(x^p)` reads as reducible for a reason unrelated to `lambda` |
| Beta-type Misiurewicz | `A` irreducible and primitive | the clean subfamily; if the census disagrees with the screen here, the census is wrong |
| Salem candidates | conjugates on the unit circle | Salem numbers exist below 2, so the screen's circle test is live rather than decorative |
| A known Pisot value | plastic constant, golden ratio | a reported Pisot hit below the golden ratio must appear on the Dufresnoy–Pisot list |

### 6. The screen is in the wrong repository for this consumer

A structural blocker, found by reading `vendored.toml` rather than the
literature. This repository vendors `finite_exact`, `claim_governance` and
`substitution_dynamics` from the kernels monorepo. It does **not** vendor
`finite_linear_algebra`, and the degree-`n` Pisot screen is not in the monorepo at
all — it lives in the Pisot repository, which this one does not vendor from.

So B8's prerequisite is delivered but unreachable from the repository that holds
the tree combinatorics. Three ways out, and the choice belongs to whoever writes
the census rather than to this note:

1. extract the screen to the kernels monorepo and vendor it here, which matches
   where the `M`-adic carrier went and keeps one implementation;
2. put the census in the Pisot repository and move the tree combinatorics to it,
   which inverts the dependency;
3. duplicate the screen here, which the vendoring policy exists to forbid.

Option 1 is the only one consistent with the standing policy. It is also not free:
the screen depends on `psc.pisot` for shared polynomial helpers, so extraction is
a real change and not a file move.

## What this gate licenses, and what it does not

1. **Licensed:** a census over a declared box of Misiurewicz types `(l, k)`,
   partitioned by whether `A_c` is primitive with irreducible characteristic
   polynomial, reporting root location where the screen decides and refusing
   where it does not.
2. **Not licensed:** any claim about which weak Perron numbers arise. Thurston
   answered the image question and this census does not touch it.
3. **Not licensed:** presenting the census, or any picture drawn from it, as the
   Thurston set or the Master Teapot. Those are closures of conjugate sets; this
   is a finite sample of a fiber.
4. **Not licensed:** reading "reducible characteristic polynomial" as "not Pisot"
   in the imprimitive case, where the factorisation `x^k P(x^p)` records the
   matrix's periodicity instead.
5. **Not licensed:** implementation before the screen is reachable. Finding 6 is a
   blocker, not a detail, and duplicating the screen to get around it is
   forbidden by the vendoring policy.
6. **Not licensed:** reporting a Pisot hit below the golden ratio without checking
   it against the known list. In that range the answer is enumerable, so an
   unlisted hit is a defect until shown otherwise.

## Sources

Retrieved 2026-09-17. Bibliographic detail is recorded as the sources present it; no PDF snapshots were imported, so nothing here is a verified snapshot.

[^1]: William P. Thurston, "Entropy in dimension one," in *Frontiers in Complex Dynamics*, Princeton University Press, 2014.
[^2]: Ethan Dickmann, Marissa Domat, Michael Hill, Sanghoon Kwak, Juliana Ospina, Priyam Patel and Alina Rechkin, "[Thurston's Theorem: Entropy in Dimension One](https://arxiv.org/abs/2209.15102)," arXiv:2209.15102. An expository modernisation; it states the weak Perron characterisation and supplies an ergodicity proof missing from the original.
[^3]: Harrison Bray, Diana Davis, Kathryn Lindsey and Chenxi Wu, "[The Shape of Thurston's Master Teapot](https://arxiv.org/pdf/1902.10805)," and "[A characterization of Thurston's Master Teapot](https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/characterization-of-thurstons-master-teapot/A24092C6CDE1AEA04E7023E59C4D9224)," *Ergodic Theory and Dynamical Systems*.
[^4]: Wolf Jung, "[Core entropy and biaccessibility of quadratic polynomials](https://arxiv.org/abs/1401.4792)," arXiv:1401.4792. The row-sum bound `1 <= lambda <= 2`, the definition of the edge transition matrix, and Lemma 3.9.4 for exactly when `A` is reducible or imprimitive.
[^5]: [Pisot number](https://mathworld.wolfram.com/PisotNumber.html), Wolfram MathWorld, for the plastic constant as the smallest Pisot number (Salem 1944, Siegel 1944), closedness of the set (Salem 1944), the golden ratio as smallest limit point, and the Dufresnoy–Pisot 1955 enumeration below it.
[^6]: Giulio Tiozzo, "[Continuity of core entropy of quadratic polynomials](https://www.math.utoronto.ca/tiozzo/docs/continuity.pdf)," *Inventiones Mathematicae*, 2016; and Kathryn Lindsey, Giulio Tiozzo and Chenxi Wu, "[Master Teapots and Entropy Algorithms for the Mandelbrot Set](https://arxiv.org/abs/2112.14590)," arXiv:2112.14590, for the principal-vein analogues.
[^7]: "[Polynomials with core entropy zero](https://arxiv.org/abs/2205.13704)," arXiv:2205.13704.
