"""Assemble the atlas page: exact numbers from Mojo, positions from here.

    python tools/atlas/build_page.py [output.html]

The split is the repository's policy, not a convenience.

Exact objects -- the catalogue and its counts, kneading sequences and internal
addresses, tuned angles, the obstruction extractions with their pairs, the
decided measures, the incidence packages -- come from one run of
`mojo src/atlas_dataset.mojo`, the canonical implementation, which
`tests/test_atlas_dataset.py` checks against the Python oracles.

Positions cannot come from there: they are floating point, and no module under
`src/` may produce one. They come from `trace_positions.py` beside this file,
and the page says so where it shows them.

The exclusion boxes are the exception that proves the split. The boxes and
their verdicts are exact, from `tools/interval_exclusion_reference.py`, the
oracle for `src/interval_orbit.mojo`; only their placement on a canvas is
floating point. Exclusion is not existence: a root in the box is a separate
witness and the page claims none.

The output is a single self-contained HTML file. It is a picture of finite
evidence and proves nothing on its own.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))

import interval_exclusion_reference as ie  # noqa: E402
import trace_positions as tp  # noqa: E402

MAX_COMPONENT_PERIOD = 5
NAMED_ROOT_RAY = {
    (1, 3): "doubling", (2, 3): "doubling", (1, 7): "rabbit", (2, 7): "rabbit",
    (3, 7): "airplane", (4, 7): "airplane", (7, 15): "primitive period 4",
    (8, 15): "primitive period 4", (2, 5): "satellite period 4", (3, 5): "satellite period 4",
}


def exact_sections() -> dict:
    """One Mojo run. Every number in the result is an integer or a rational."""
    done = subprocess.run(["mojo", "src/atlas_dataset.mojo"], cwd=ROOT,
                          capture_output=True, text=True, check=True)
    return json.loads(done.stdout)


def traced_addresses(catalogues: list[dict]) -> list[dict]:
    """Each catalogue address traced to a position and finished on its equation."""
    out = []
    for row in catalogues:
        preperiod, period, den = row["l"], row["k"], row["den"]
        for num in row["addresses"]:
            landed = tp.trace_ray(Fraction(num, den), depth=22)
            if landed is None:
                continue
            polished = tp.polish_misiurewicz(landed, preperiod, period)
            moved = abs(polished - landed) if polished is not None else -1.0
            if polished is not None and tp.satisfies_type(polished, preperiod, period):
                landed = polished
            out.append({"num": num, "den": den, "l": preperiod, "k": period,
                        "re": round(landed.real, 12), "im": round(landed.imag, 12),
                        "agrees": tp.satisfies_type(landed, preperiod, period),
                        "moved": round(moved, 12)})
    return out


def traced_components() -> list[dict]:
    """Root rays traced and met at one centre, which is what groups them."""
    found: dict[tuple, dict] = {}
    for period in range(1, MAX_COMPONENT_PERIOD + 1):
        den = 2 ** period - 1
        for num in range(1, den):
            theta = Fraction(num, den)
            if tp.period_of(theta) != period:
                continue
            landed = tp.trace_ray(theta, depth=18)
            centre = tp.newton_center(landed, period) if landed is not None else None
            if centre is None:
                continue
            key = (period, round(centre.real, 6), round(centre.imag, 6))
            entry = found.setdefault(key, {"period": period, "re": round(centre.real, 12),
                                           "im": round(centre.imag, 12), "rays": [], "name": None})
            entry["rays"].append([num, den])
            if (num, den) in NAMED_ROOT_RAY:
                entry["name"] = NAMED_ROOT_RAY[(num, den)]
    found[(1, 0.0, 0.0)] = {"period": 1, "re": 0.0, "im": 0.0, "rays": [[0, 1]],
                            "name": "main cardioid"}
    return sorted(found.values(), key=lambda e: (e["period"], e["re"], e["im"]))


def place_tunings(tunings: list[dict]) -> None:
    """A tuned angle is exact; the component it names still has to be found."""
    for row in tunings:
        if row["tuned"] is None or not row["period"]:
            row["re"] = row["im"] = None
            continue
        landed = tp.trace_ray(Fraction(*row["tuned"]), depth=18)
        centre = tp.newton_center(landed, row["period"]) if landed is not None else None
        row["re"] = round(centre.real, 12) if centre else None
        row["im"] = round(centre.imag, 12) if centre else None


def box_record(name: str, box, preperiod: int, period: int, horizon: int,
               angles: list[Fraction], note: str) -> dict:
    excluded, forbidden, failures = ie.excluded_count(box, preperiod, period, horizon)
    return {"name": name, "l": preperiod, "k": period, "horizon": horizon,
            "re": [str(box.re.lo), str(box.re.hi)], "im": [str(box.im.lo), str(box.im.hi)],
            "re_f": [float(box.re.lo), float(box.re.hi)],
            "im_f": [float(box.im.lo), float(box.im.hi)],
            "excluded": excluded, "forbidden": forbidden,
            "failures": [list(f) for f in failures],
            "theta": [[a.numerator, a.denominator] for a in angles], "note": note}


def certificates(addresses: list[dict]) -> list[dict]:
    """The two pinned boxes, a horizon control, and one box per further type."""
    rows = [
        box_record("c = -2", ie.c_minus_2_box(), 2, 1, 3, [Fraction(1, 2)],
                   "the repository's minimal smoke test: half-width 1/16 about -2"),
        box_record("c = -2, one step further", ie.c_minus_2_box(), 2, 1, 4, [Fraction(1, 2)],
                   "computed here: the same box at horizon 4. Exclusion is relative to a horizon, "
                   "and this box is too wide to decide the two collisions the extra step introduces"),
        box_record("M(4,1)", ie.m41_box(), 4, 1, 6,
                   [Fraction(9, 56), Fraction(11, 56), Fraction(15, 56)],
                   "the repository's stress test: half-width 2^-25, three rays landing together"),
    ]
    seen: set[tuple[int, int]] = set()
    for row in addresses:
        preperiod, period = row["l"], row["k"]
        if (preperiod, period) in seen or preperiod + period > 5 or not row["agrees"]:
            continue
        # The critical-orbit preperiod is one more than the angle's own.
        ell, horizon = preperiod + 1, preperiod + 1 + period + 1
        for half_exp in range(6, 34):
            centre_exp = half_exp + 4
            box = ie.dyadic_box(round(row["re"] * 2 ** centre_exp),
                                round(row["im"] * 2 ** centre_exp), centre_exp, half_exp)
            if not ie.excluded_count(box, ell, period, horizon)[2]:
                rows.append(box_record(
                    f"({preperiod},{period}) at {row['num']}/{row['den']}", box, ell, period,
                    horizon, [Fraction(row["num"], row["den"])],
                    "computed here: the widest dyadic box about the traced position that "
                    "excludes every forbidden collision"))
                seen.add((preperiod, period))
                break
    return rows


def main() -> int:
    data = exact_sections()
    data["misiurewicz"] = traced_addresses(data["catalogues"])
    data["components"] = traced_components()
    place_tunings(data["tunings"])
    data["certificates"] = certificates(data["misiurewicz"])

    page = (HERE / "head.html").read_text(encoding="utf-8") + \
           (HERE / "body.html").read_text(encoding="utf-8") + \
           (HERE / "script.html").read_text(encoding="utf-8").replace(
               "__DATA__", json.dumps(data, separators=(",", ":")))
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "atlas.html"
    out.write_text(page, encoding="utf-8")

    disagreeing = [row for row in data["misiurewicz"] if not row["agrees"]]
    print(f"exact sections from Mojo: "
          f"{ {name: len(rows) for name, rows in data.items() if isinstance(rows, list)} }")
    print(f"traced addresses: {len(data['misiurewicz'])}, "
          f"disagreeing with their exact type: {len(disagreeing)}")
    print(f"components: {len(data['components'])}, certificates: {len(data['certificates'])}")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 1 if disagreeing else 0


if __name__ == "__main__":
    raise SystemExit(main())
