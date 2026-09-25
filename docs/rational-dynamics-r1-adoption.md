# Shared rational-dynamics R1 adoption

**Status:** differential integration only; no theorem-status or certificate-authority change.

This branch vendors `rational_dynamics/` from
`larsbx/finite-math-kernels` PR #33 at commit

```text
dfe9e6f627690f2ca72a38150f32de7bea461494
```

The upstream commit passed the default CI, Julia parallel gate, and frontier
polyglot gate before this pin was created.

## What is shared

The package owns exact finite arithmetic on reduced nonnegative fractions:

- normalization over the unbounded `BigZ` backend;
- doubling modulo one;
- modular inverse and centered modular inverse;
- simple continued fractions and convergents;
- Farey determinant / adjacency arithmetic.

It owns no parameter-plane interpretation.

## Consumer gate

`src/rational_dynamics_bridge.mojo` compares the shared package with the
existing `BigQRayAddr` implementation on the overlapping operation
(doubling modulo one) and separately replays the new modular-inverse,
continued-fraction, convergent, and Farey primitives.

The existing `BigQRayAddr` path remains the consumer's current
acceptance-bearing implementation. Shared-kernel agreement is differential
evidence only. A later migration must explicitly change that authority
boundary rather than acquiring it merely by vendoring the package.

## Why this is useful now

The same fraction arithmetic is used independently by the Ford/bulb research
program. Pinning the neutral kernel here means the parameter-plane symbolic
address layer and the Ford arithmetic can now be compared against one finite
contract without importing either domain's conclusions into the other.
