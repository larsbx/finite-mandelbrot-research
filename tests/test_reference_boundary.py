"""Estate reference-plane boundary."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    "tools/poly_reference.py": "reference/python/polynomial/poly_reference.py",
    "tools/interval_exclusion_reference.py": "reference/python/interval/interval_exclusion_reference.py",
    "tools/carrier_density_profile_reference.py": "reference/python/c1/carrier_density_profile_reference.py",
    "tools/misiurewicz_catalogue_reference.py": "reference/python/c1/misiurewicz_catalogue_reference.py",
    "tools/misiurewicz_prefix_graph_reference.py": "reference/python/c1/misiurewicz_prefix_graph_reference.py",
    "tools/separated_density_reference.py": "reference/python/c1/separated_density_reference.py",
    "tools/kneading_reference.py": "reference/python/c1/kneading_reference.py",
    "tools/exact_arithmetic_property_oracle.py": "reference/python/arithmetic/exact_arithmetic_property_oracle.py",
}


def test_reference_implementations_live_in_the_reference_plane():
    for shim, canonical in MAPPINGS.items():
        canonical_path = ROOT / canonical
        assert canonical_path.is_file(), canonical
        assert len(canonical_path.read_text(encoding="utf-8").splitlines()) > 40


def test_tools_entrypoints_are_only_compatibility_shims():
    for shim, canonical in MAPPINGS.items():
        body = (ROOT / shim).read_text(encoding="utf-8")
        assert canonical in body
        assert "Compatibility shim" in body
        assert len(body.splitlines()) < 30, shim


def test_ci_uses_reference_plane_not_compatibility_shims():
    workflow = (ROOT / ".github" / "workflows" / "no-trig-audit.yml").read_text(encoding="utf-8")
    assert "reference/python/polynomial/poly_reference.py" in workflow
    assert "reference/python/interval/interval_exclusion_reference.py" in workflow
    assert "reference/python/c1/carrier_density_profile_reference.py" in workflow
    assert "tools/poly_reference.py" not in workflow
    assert "tools/interval_exclusion_reference.py" not in workflow


def test_carrier_density_direct_execution_does_not_need_the_shim(tmp_path):
    """The canonical entrypoint must resolve its sibling even without the shim."""
    canonical_dir = tmp_path / "reference" / "python" / "c1"
    canonical_dir.mkdir(parents=True)
    for name in ("carrier_density_profile_reference.py", "separated_density_reference.py"):
        shutil.copy2(ROOT / "reference" / "python" / "c1" / name, canonical_dir / name)

    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    shutil.copytree(ROOT / "tools" / "oracle_refinement", tools_dir / "oracle_refinement")
    assert not (tools_dir / "separated_density_reference.py").exists()

    result = subprocess.run(
        [sys.executable, str(canonical_dir / "carrier_density_profile_reference.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
