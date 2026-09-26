# Repository architecture

This repository is the first adopter of the estate repository template.

The machine-readable source of repository structure and authority is
[`estate.toml`](estate.toml). The reusable v1 contract and audit are pinned from
`larsbx/finite-math-kernels/audit/estate_repository/v1` by the `[estate_tooling]`
table in `estate.toml`. This repository's staged application is
[`docs/architecture/finite-mandelbrot-application.md`](docs/architecture/finite-mandelbrot-application.md).

The ordering rule is:

```text
authority -> mathematical/domain concern -> implementation language
```

The current tree is intentionally transitional. Existing paths remain authoritative
until a dedicated migration PR moves them. Directory renames alone must not change
theorem status, certificate acceptance, imported-theorem assumptions, or the
Mojo finite-checker boundary.
