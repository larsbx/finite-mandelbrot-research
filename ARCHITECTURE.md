# Repository architecture

This repository is the first adopter of the estate repository template.

The machine-readable source of repository structure and authority is
[`estate.toml`](estate.toml). The reusable contract is
[`docs/architecture/estate-repository-template-v1.md`](docs/architecture/estate-repository-template-v1.md),
and this repository's staged application is
[`docs/architecture/finite-mandelbrot-application.md`](docs/architecture/finite-mandelbrot-application.md).

The ordering rule is:

```text
authority -> mathematical/domain concern -> implementation language
```

The current tree is intentionally transitional. Existing paths remain authoritative
until a dedicated migration PR moves them. Directory renames alone must not change
theorem status, certificate acceptance, imported-theorem assumptions, or the
Mojo finite-checker boundary.
