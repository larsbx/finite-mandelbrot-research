from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TOOLING_REVISION = "7543130ccfa05a88b5ddbacb46d4371ac99c21f9"


def load_manifest():
    return tomllib.loads((ROOT / "estate.toml").read_text(encoding="utf-8"))


def test_estate_manifest_names_canonical_repository():
    data = load_manifest()
    assert data["repository"]["id"] == "larsbx/finite-mandelbrot-research"
    assert data["principles"]["ordering"] == ["authority", "domain", "language"]


def test_shared_estate_tooling_is_immutably_pinned():
    data = load_manifest()
    assert data["estate_tooling"] == {
        "repository": "larsbx/finite-math-kernels",
        "path": "audit/estate_repository/v1",
        "revision": TOOLING_REVISION,
    }


def test_only_mojo_has_acceptance_authority():
    data = load_manifest()
    accepted = [x["name"] for x in data["language"] if x["acceptance_authority"]]
    assert accepted == ["Mojo"]


def test_julia_oracle_lane_remains_supporting():
    assert (ROOT / "oracles" / "julia").is_dir()
    data = tomllib.loads((ROOT / "polyglot.manifest.toml").read_text(encoding="utf-8"))
    assert "Julia" in data["authority"]["supporting_languages"]


def test_template_forbids_empty_silos_and_mass_move():
    data = load_manifest()
    assert data["principles"]["empty_silos"] == "forbidden"
    assert data["migration"]["mass_move"] is False
