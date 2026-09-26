from pathlib import Path
import importlib.util
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def load_audit_module():
    path = ROOT / "tools" / "audit_estate_layout.py"
    spec = importlib.util.spec_from_file_location("audit_estate_layout", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_estate_manifest_is_valid():
    audit = load_audit_module()
    audit.validate(audit.load())


def test_estate_manifest_names_canonical_repository():
    data = tomllib.loads((ROOT / "estate.toml").read_text(encoding="utf-8"))
    assert data["repository"]["id"] == "larsbx/finite-mandelbrot-research"
    assert data["principles"]["ordering"] == ["authority", "domain", "language"]


def test_only_mojo_has_acceptance_authority():
    data = tomllib.loads((ROOT / "estate.toml").read_text(encoding="utf-8"))
    accepted = [x["name"] for x in data["language"] if x["acceptance_authority"]]
    assert accepted == ["Mojo"]


def test_template_forbids_empty_silos_and_mass_move():
    data = tomllib.loads((ROOT / "estate.toml").read_text(encoding="utf-8"))
    assert data["principles"]["empty_silos"] == "forbidden"
    assert data["migration"]["mass_move"] is False
