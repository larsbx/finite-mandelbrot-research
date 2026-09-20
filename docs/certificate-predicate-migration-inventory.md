# Certificate predicate migration inventory

Status: executable-boundary inventory during BigZ-backed c=-2 replay.

This inventory separates finite computations, imported classical results, and
the global C1 obligation. A green bounded-width computation is not a
proof-grade certificate and cannot discharge an imported theorem or C1.

| Predicate | Current executable source | State | Acceptance consequence |
| --- | --- | --- | --- |
| Squarefree `P_{2,1}` evaluation and strict localization | `src/krawczyk_witness.mojo` | replayed on unbounded BigZ rational intervals; rejection distinct from non-contraction | accepts the finite arithmetic replay only; proof-grade acceptance is explicitly false |
| Same-box forbidden collisions | `src/interval_orbit.mojo` | replayed 5/5 on the same parameterized BigZ box constructor as localization; rejection distinct from ambiguity | accepts the finite exact-type arithmetic replay only |
| Rational ray-address orbit for `1/2` | `src/bigq_ray_address.mojo` | replayed with normalized BigZ-backed `Q`, including a representation whose inputs exceed `Int64`; malformed and out-of-range values reject | accepts finite symbolic address data only |
| Rational parameter-ray landing replay | `src/bigq_landing_target_adapter.mojo` | composes same-exponent BigZ localization, exact-type exclusion, and symbolic address replay; correspondence citation remains metadata | finite replay only; retained as a non-acceptance-bearing cross-check |
| Proof-grade rational landing target association | `src/proof_grade_landing_target_association.mojo` | exact BigZ/Q ray orbit, exact BigZ replay of `R_{2,1}=C^3(C+2)`, lower-type exclusion of `C=0`, exact type `(2,1)` at `C=-2`, and canonical checked theorem import | proof-grade target association accepted for the `c=-2`, address-`1/2` payload |
| Legacy BigQ theorem payload replay | `src/bigq_theorem_tag_payload_instances.mojo` | finite source scope matched with classification attachment deliberately absent | remains non-final; superseded for the acceptance-bearing rational landing path by the proof-grade association module |
| Known trivial-fiber class import | `src/bigq_theorem_tag_payload_instances.mojo` | BigZ/Q Misiurewicz instance data matched; classification proof attachment explicitly absent | final import remains false |
| Finite-certificate composition | `src/bigq_finite_certificate_gate.mojo` | BigZ/Q finite inputs compose at standard and beyond-`Int64` widths; ambiguity and invalid widths reject | theorem tags and complete certificate acceptance remain false |
| Incidence packaging | `src/bigq_certificate_incidence.mojo` | compiler-wired carrier stores three explicit finite vertices and validates their roles and distinctness | finite incidence may package; certificate emission remains false |
| Squarefree `P_{2,1}` evaluation and strict localization | `src/checked_krawczyk_witness.mojo` | computed, checked-width | accepts bounded localization only |
| Same-box forbidden collisions | `src/checked_interval_exclusion.mojo` | computed 5/5, checked-width | accepts bounded exact-type evidence only |
| Joint arithmetic localization | `src/certificate_arithmetic_migration_gate.mojo` | computed, same-box, checked-width | proof-grade acceptance remains false |
| Rational ray-address orbit for `1/2` | `src/checked_ray_address.mojo` | computed preperiod 1, period 1; overflow rejects | accepts bounded finite ray data only |
| Rational parameter-ray landing target | `src/checked_landing_target_adapter.mojo` | exact `P_{2,1}` factorization, lower-type rejection, ray orbit, and source correspondence checked at bounded width | proof-grade association remains false |
| Rational parameter-ray landing import | `src/C1_theorem_tag_payload_instances.mojo` | source metadata checked independently; bounded-width association retained as a cross-check; final path consumes `ProofGradeLandingTargetAssociation` | final import admissible for the `c=-2`, address-`1/2` instance |
| Known trivial-fiber class import | `src/C1_theorem_tag_payload_instances.mojo` | Misiurewicz source scope matched at checked width; proof-grade classification absent | blocks finite-certificate acceptance |
| Checked finite-certificate composition | `src/checked_finite_certificate_gate.mojo` | finite inputs accepted; rational landing tag accepted; Misiurewicz trivial-fiber tag still rejected | full certificate remains rejected |
| Incidence packaging | legacy `src/certificate_incidence.mojo` | size-only carrier, not in the compiler-wired acceptance path | retained for comparison; superseded by explicit BigZ-path carrier |
| Integer backend | `src/bigint_z.mojo` | dynamic limbs with exact ring/order/division/gcd and canonical integer serialization | rational and core intervals migrated; remaining consumers still block proof-grade acceptance |
| `ResidualClosureNoMissingLinks` | `src/C1_residual_closure_no_missing_links.mojo` | open | blocks C1 independently of finite certificates |

## Next obligations

1. Attach and validate the class-specific Misiurewicz trivial-fiber theorem
   payload for the exact type-`(2,1)` `c=-2` instance. The rational landing
   import is no longer the blocker.
2. Define canonical serialization for the explicit finite incidence carrier
   before any certificate artifact can be hashed or replayed across processes.
3. Keep the C1 residual-closure proof track separate; no finite example,
   accepted landing import, or successful certificate instance implies the
   missing global closure statement.
