# Repository migration provenance

This repository is the dedicated home for the finite-regime Mandelbrot research program.

The migration is pinned to `larsbx/NLAP-JT` source commit `d00c64d4ec703564a2d8ceb606279d2025f2352a`. The source history is imported with `.github/workflows/` removed from the imported commit graph solely because the GitHub Actions token used for the history join has `contents: write` but not GitHub's separate workflow-write permission. No research, source, test, paper, specification, or governance content is omitted by that sanitization. The canonical workflow is restored on the migration branch through GitHub's authorized contents API after the history push.

Consumer-owned current-tree repository identity is migrated to `larsbx/finite-mandlebrot-research`. Mathematical claims and proof status are unchanged by the repository move. In particular, the exact rational/interval arithmetic boundary, no-transcendental-trigonometry policy, no-circle/rank-2 rule, no-ideal-point rule, Mojo-first theorem-kernel policy, theorem-tag imports, and C1 open-frontier status remain binding.

Vendored code under `src/finite_exact/` and `tools/claim_governance/` is intentionally byte-for-byte preserved so that the SHA-256 pins in `vendored.toml` remain valid. A vendored upstream comment may therefore retain the former consumer name until the upstream `finite-math-kernels` package is revised and re-pinned.

The original `larsbx/NLAP-JT` name is otherwise retained only here as provenance for the imported history.
