"""
sauna_engine.py — build orchestrator for an outdoor sauna envelope.

This is the layer that defines a concrete build (assemblies + interface
details), reconciles every interface off ONE datum per assembly via planes.py,
runs validation, and is the single place a DXF emitter would hook in.

The markdown blueprint in docs/ describes an INDOOR electric reference sauna.
This engine handles the OUTDOOR rainscreen-clad variant, where the envelope
detailing (out-sulation, drainage cavity, fascia/jamb/threshold reconciliation)
is the hard part. The two are complementary: docs/ = what to build, this = the
arithmetic that keeps the construction details from contradicting each other.

Run:  python3 sauna_engine.py
"""

from __future__ import annotations
from dataclasses import dataclass, field

from planes import (
    inch, Assembly, FasciaDetail, DoorJamb, Threshold,
    Issue, run_validation, report, assert_coplanar,
)
from drawing import (
    Room, wall_section, jamb_plan, threshold_section, floor_plan, save_set,
)


# ---------------------------------------------------------------------------
# A named build = one or more assemblies + the interface details that reconcile
# ---------------------------------------------------------------------------
@dataclass
class SaunaBuild:
    name: str
    wall: Assembly
    details: list = field(default_factory=list)
    room: "Room | None" = None

    def validate(self) -> list[Issue]:
        issues = run_validation(*self.details)
        # Cross-detail: the front line every detail must agree on.
        planes = {"cladding": self.wall.cladding_plane}
        for d in self.details:
            if isinstance(d, FasciaDetail):
                planes["fascia"] = d.fascia_face
        if len(planes) >= 2:
            issues += assert_coplanar(f"{self.name}:front-plane",
                                      tol=self.wall.tol, **planes)
        return issues

    def report(self) -> bool:
        print(self.wall.table())
        print()
        return report(self.validate())

    def sheets(self) -> list:
        """Build the drawing set from the validated model (same numbers)."""
        out = []
        if self.room is not None:
            out.append(floor_plan(self.room, number="A-0"))
        out.append(wall_section(self.wall, number="A-1"))
        for d in self.details:
            if isinstance(d, DoorJamb):
                out.append(jamb_plan(d, number="A-2"))
            elif isinstance(d, Threshold):
                out.append(threshold_section(d, number="A-3"))
        return out

    def emit_drawings(self, outdir: str = "drawings") -> dict:
        """Render the blueprint set to SVG (+ PDF if cairosvg is present)."""
        written = save_set(self.sheets(), outdir)
        n_svg, n_pdf = len(written["svg"]), len(written["pdf"])
        print(f"[draw] wrote {n_svg} SVG"
              + (f" + {n_pdf} PDF sheet(s)" if n_pdf else " (no PDF — cairosvg "
                 "not installed; open the SVG/index.html and print to PDF)")
              + f" to ./{outdir}/  (open {outdir}/index.html)")
        return written


# ---------------------------------------------------------------------------
# Reference outdoor build: out-sulated rainscreen, thermo-aspen slat cladding
# ---------------------------------------------------------------------------
# An INDEPENDENT record of what the existing drawing set claims for the front
# interfaces. In production this comes from the DXF you already emitted / a shop
# ticket — NOT re-derived from the wall here. Feeding it as expect= turns the
# guards into a real reconciliation: if the model and this record ever diverge,
# validation CLASHes. (Edit any value to a wrong number to see it fire.)
EXTERNAL_AS_DRAWN = {
    "fascia_face": inch(3.75),          # 95.2 mm
    "jamb_extension": inch(3.75),
    "threshold_extension": inch(3.75),
}


def reference_build(external: dict | None = None) -> SaunaBuild:
    ext = external or {}
    wall = (Assembly("outdoor sauna wall", "exterior face of 1/2\" ZIP sheathing")
            .add("exterior insulation (Comfortboard)", inch(1.5))
            .add("rainscreen furring v (drainage)", inch(0.75), is_drainage_gap=True)
            .add("cross furring h (slat substructure)", inch(0.75))
            .add("dark slat cladding (thermo-aspen)", inch(0.75)))

    details = [
        FasciaDetail(wall=wall, base_fascia_face=inch(0.5),
                     expect_face=ext.get("fascia_face")),
        DoorJamb(wall=wall, frame_face=inch(0.0),
                 casing="proud", proud_reveal=inch(0.125),
                 expect_extension=ext.get("jamb_extension")),
        Threshold(wall=wall, frame_sill_face=inch(0.0), interior_floor_top=0.0,
                  step_down=inch(0.5), pan_slope_pct=4.0,  # 4% clears min fall
                  expect_extension=ext.get("threshold_extension")),
    ]
    # Interior plan figures (the docs/ reference: 6 x 5 x 7 ft).
    room = Room(name="outdoor-reference (6x5x7 ft)",
                width=inch(72), depth=inch(60), height=inch(84),
                bench_upper_depth=inch(24), bench_lower_depth=inch(18),
                door_width=inch(24))
    return SaunaBuild("outdoor-reference", wall, details, room=room)


def main() -> int:
    # Reconcile the model against the independently-maintained drawing record.
    build = reference_build(external=EXTERNAL_AS_DRAWN)
    ok = build.report()
    if ok:
        build.emit_drawings("drawings")   # only draw a clash-free model
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
