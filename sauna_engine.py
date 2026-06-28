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


# ---------------------------------------------------------------------------
# A named build = one or more assemblies + the interface details that reconcile
# ---------------------------------------------------------------------------
@dataclass
class SaunaBuild:
    name: str
    wall: Assembly
    details: list = field(default_factory=list)

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
        ok = report(self.validate())
        if ok:
            self.emit_dxf()
        return ok

    def emit_dxf(self) -> None:
        # TODO(ezdxf): emit wall section + plan with every plane driven off
        # the same offsets used above, so the drawing cannot diverge from the
        # validated model. Hook a real writer here once a clean result is
        # required before drawings are produced.
        print(f"[dxf] (stub) would emit '{self.name}' — model is clash-free.")


# ---------------------------------------------------------------------------
# Reference outdoor build: out-sulated rainscreen, thermo-aspen slat cladding
# ---------------------------------------------------------------------------
def reference_build() -> SaunaBuild:
    wall = (Assembly("outdoor sauna wall", "exterior face of 1/2\" ZIP sheathing")
            .add("exterior insulation (Comfortboard)", inch(1.5))
            .add("rainscreen furring v (drainage)", inch(0.75), is_drainage_gap=True)
            .add("cross furring h (slat substructure)", inch(0.75))
            .add("dark slat cladding (thermo-aspen)", inch(0.75)))

    details = [
        FasciaDetail(wall=wall, base_fascia_face=inch(0.5)),
        DoorJamb(wall=wall, frame_face=inch(0.0),
                 casing="proud", proud_reveal=inch(0.125)),
        Threshold(wall=wall, frame_sill_face=inch(0.0), interior_floor_top=0.0,
                  step_down=inch(0.5), pan_slope_pct=4.0),  # 4% clears min fall
    ]
    return SaunaBuild("outdoor-reference", wall, details)


def main() -> int:
    build = reference_build()
    ok = build.report()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
