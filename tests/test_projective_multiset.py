from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "projective_multiset.mojo"
SPEC = ROOT / "docs" / "projective-multiset.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_projective_morphism_and_infinity_multiplicity_are_explicit():
    spec = read(SPEC)
    source = read(SOURCE)
    assert "F_c [X:Z] = [X^2 + c Z^2 : Z^2]" in spec
    assert "(F_c^n)^* [infinity] = 2^n [infinity]" in spec
    assert "def infinity_pullback_multiplicity" in source
    assert "return 1 << iterates" in source


def test_affine_landing_is_separated_from_algebraic_escape():
    spec = read(SPEC)
    source = read(SOURCE)
    assert "an affine orbit" in spec
    assert "never lands on the infinity divisor" in spec
    assert "def affine_orbit_lands_at_infinity" in source
    assert "return False" in source


def test_multiset_coefficient_has_declared_semantics_and_grading():
    spec = read(SPEC)
    source = read(SOURCE)
    assert "critical-basin multiplicity" in spec
    assert "graded by the exact critical-orbit signature" in spec
    assert "struct ParameterCycle" in source
    assert "var multiplicity: Int" in source
    assert "var tail: Int" in source
    assert "var period: Int" in source


def test_claim_firewall_is_explicit():
    spec = " ".join(read(SPEC).split())
    assert "does not identify a finite-field shadow with the classical Mandelbrot set" in spec
    assert "local connectivity, fibre triviality, or landing of external rays" in spec
    assert "Supporting general prime powers" in spec
