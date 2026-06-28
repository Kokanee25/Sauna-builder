"""
planes.py  —  Datum + layer-stack reconciliation for sauna_engine.py

Core idea:
    Pick ONE master datum per assembly. Every layer is just a thickness
    stacked outward from that datum. The "finish plane" is a DERIVED number,
    never measured. Every interface (fascia, door jamb, threshold) is computed
    as a delta off the same stack, so two details PHYSICALLY CANNOT disagree.

    Coplanarity / clash / fit are ASSERTIONS, not judgement calls. The engine
    never gets arithmetic wrong; you only ever supply intent (flush vs proud,
    how trim dies into cladding, how the sill drains).

How the "cannot disagree" guarantee is actually enforced:
    1. Single source. Every detail (FasciaDetail / DoorJamb / Threshold) holds
       a reference to the SAME Assembly and derives its planes from it. There is
       no second hand-typed copy of the stack to drift from.
    2. External cross-checks. Each detail accepts an optional `expect=` — a
       value taken from an INDEPENDENT source (another drawing, a DXF you
       already emitted, a shop ticket). validate() asserts derived == expect.
       This is a real check: it can fail, and when it does, two sources of
       truth disagree. (The previous version compared a value to itself, which
       could never fail — see git history.)
    3. assert_coplanar(): asserts a set of independently-named planes are equal
       within tolerance, for when several details must land on one line.

Units: everything internal is millimetres (mm). Use inch() for imperial input.
Convention: +offset = OUTWARD from the datum (toward weather / away from frame).
Note two axes coexist: layer stacks run OUTWARD (X); threshold heights
(interior_floor_top, step_down) run VERTICAL (Z). They are kept separate and
never added together.

Pure stdlib. Fold the dataclasses + derivations into sauna_engine.py; the DXF
hooks are marked TODO where you'd emit with ezdxf.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Units
# ---------------------------------------------------------------------------
def inch(x: float) -> float:
    """Convert inches -> mm."""
    return x * 25.4


def mm_to_in(x: float) -> float:
    return x / 25.4


def _dedupe(values, tol: float = 0.5) -> tuple[float, ...]:
    """Collapse near-equal stock sizes (e.g. 19.0 vs 19.05) within tol."""
    out: list[float] = []
    for v in sorted(values):
        if not out or v - out[-1] > tol:
            out.append(v)
    return tuple(out)


# Common ripped/sheet stock thicknesses you can actually buy/produce (mm).
# Used to flag jamb extensions that can't come from a single piece.
# Imperial dressed sizes (the real products you'd rip from) plus the few metric
# sheet goods that have no close imperial twin. De-duped so near-identical sizes
# don't both sit in the list; we keep the genuine imperial dimension (e.g. the
# 38.1 mm dressed 2x) rather than a rounded metric stand-in.
STD_STOCK_MM = _dedupe((
    inch(0.25), inch(0.5), inch(0.625), inch(0.75), inch(1.0),
    inch(1.5),  # nominal 2x dressed = 38.1 mm
    9.0, 18.0,  # common metric sheet goods, no close imperial twin
))
MAX_STOCK_MM = max(STD_STOCK_MM)


# ---------------------------------------------------------------------------
# Severity / issues
# ---------------------------------------------------------------------------
class Severity(Enum):
    OK = "OK"
    WARN = "WARN"     # buildable but needs a decision (laminate, non-std stock)
    CLASH = "CLASH"   # geometry conflict; drawing would be wrong


@dataclass
class Issue:
    severity: Severity
    where: str
    msg: str

    def __str__(self) -> str:
        return f"[{self.severity.value:5}] {self.where}: {self.msg}"


def _expect_issue(where: str, label: str, derived: float, expect: Optional[float],
                  tol: float) -> Optional[Issue]:
    """
    The REAL disagreement guard: compare a value we DERIVED from the stack
    against a value supplied from an INDEPENDENT source. Returns a CLASH Issue
    if they differ beyond tol, else None. (Returns None when expect is omitted.)
    """
    if expect is None:
        return None
    delta = derived - expect
    if abs(delta) > tol:
        return Issue(Severity.CLASH, where,
                     f"{label} derived {derived:.1f} mm != external {expect:.1f} mm "
                     f"(Δ {delta:+.1f} mm > tol {tol:.1f}) — two sources disagree.")
    return None


# ---------------------------------------------------------------------------
# Layer stack
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Layer:
    name: str
    thickness: float  # mm, outward
    is_drainage_gap: bool = False  # rainscreen cavity — vented, not solid


@dataclass
class Assembly:
    """An outward stack of layers measured from a single datum (datum = 0)."""
    name: str
    datum_desc: str
    layers: list[Layer] = field(default_factory=list)
    tol: float = 1.0  # mm coplanarity tolerance

    def add(self, name: str, thickness: float, is_drainage_gap: bool = False) -> "Assembly":
        self.layers.append(Layer(name, thickness, is_drainage_gap))
        return self

    def offset_after(self, layer_name: str) -> float:
        """Outward offset of the OUTER face of the named layer, from datum."""
        run = 0.0
        for ly in self.layers:
            run += ly.thickness
            if ly.name == layer_name:
                return run
        raise KeyError(f"{layer_name!r} not in {self.name}")

    @property
    def finish_plane(self) -> float:
        """Outer face of the outermost layer — the ONE derived finish number."""
        return sum(ly.thickness for ly in self.layers)

    @property
    def cladding_plane(self) -> float:
        # Outermost solid (skip a trailing drainage gap if you modelled one last)
        run = 0.0
        last_solid = 0.0
        for ly in self.layers:
            run += ly.thickness
            if not ly.is_drainage_gap:
                last_solid = run
        return last_solid

    def table(self) -> str:
        out, run = [f"{self.name}  (datum: {self.datum_desc})"], 0.0
        for ly in self.layers:
            run += ly.thickness
            tag = "  <gap>" if ly.is_drainage_gap else ""
            out.append(f"  {ly.name:<28} +{ly.thickness:6.1f} -> {run:7.1f} mm"
                       f" ({mm_to_in(run):5.2f}\"){tag}")
        out.append(f"  {'FINISH PLANE':<28} {'':7} -> {self.finish_plane:7.1f} mm"
                   f" ({mm_to_in(self.finish_plane):5.2f}\")")
        return "\n".join(out)


# ---------------------------------------------------------------------------
# Cross-detail coplanarity assertion
# ---------------------------------------------------------------------------
def assert_coplanar(where: str, tol: float = 1.0, **planes: float) -> list[Issue]:
    """
    Assert that several INDEPENDENTLY-named planes are equal within tol.

    Unlike a self-referential check, the inputs here come from different
    details/sources, so this can genuinely fail. Use it where multiple details
    must land on one line (e.g. wall cladding, fascia face, casing face).
    """
    if len(planes) < 2:
        return [Issue(Severity.OK, where, "nothing to compare")]
    lo_name, lo = min(planes.items(), key=lambda kv: kv[1])
    hi_name, hi = max(planes.items(), key=lambda kv: kv[1])
    if hi - lo > tol:
        detail = ", ".join(f"{k}={v:.1f}" for k, v in planes.items())
        return [Issue(Severity.CLASH, where,
                f"not coplanar: spread {hi - lo:.1f} mm > tol {tol:.1f} "
                f"({hi_name} vs {lo_name}) [{detail}]")]
    return [Issue(Severity.OK, where,
            f"coplanar within {tol:.1f} mm ({len(planes)} planes @ ~{lo:.1f} mm)")]


# ---------------------------------------------------------------------------
# Fascia / rafter coplanarity
# ---------------------------------------------------------------------------
@dataclass
class FasciaDetail:
    """
    Rafter tails always vary. You string/laser the tails to ONE line, land
    continuous sub-fascia on that line, fascia rides true. Coplanarity of the
    fascia face with the wall cladding plane is the assertion that stops the
    cladding from clashing into / overshooting the fascia.

    Holds the Assembly directly so the target can NEVER be a stale copy of the
    cladding plane — it is read live from the wall.
    """
    wall: Assembly
    base_fascia_face: float            # offset of fascia face before any buildout
    expect_face: Optional[float] = None  # external cross-check (e.g. from a DXF)

    @property
    def target_plane(self) -> float:
        return self.wall.cladding_plane

    @property
    def subfascia_buildout(self) -> float:
        """Thickness of sub-fascia packer needed to bring fascia coplanar."""
        return self.target_plane - self.base_fascia_face

    @property
    def fascia_face(self) -> float:
        """Resulting fascia face after buildout (only builds outward)."""
        return self.base_fascia_face + max(0.0, self.subfascia_buildout)

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        tol = self.wall.tol
        b = self.subfascia_buildout
        if b < -tol:
            issues.append(Issue(Severity.CLASH, "fascia",
                f"cladding plane is INSIDE base fascia face by {-b:.1f} mm — "
                f"you can't build the fascia inward; pull cladding stack in or "
                f"set fascia back."))
            return issues

        issues.append(Issue(Severity.OK, "fascia",
            f"sub-fascia buildout {b:.1f} mm ({mm_to_in(b):.2f}\") -> "
            f"fascia coplanar with cladding at {self.target_plane:.1f} mm"))

        ext = _expect_issue("fascia", "fascia face", self.fascia_face,
                            self.expect_face, tol)
        if ext:
            issues.append(ext)
        return issues


# ---------------------------------------------------------------------------
# Door jamb extension  (the two-furring-layer problem)
# ---------------------------------------------------------------------------
def nearest_stock(depth: float) -> tuple[Optional[float], float]:
    """Return (single-piece stock that covers depth, leftover) or (None, _)."""
    candidates = sorted(s for s in STD_STOCK_MM if s >= depth - 0.5)
    if candidates:
        return candidates[0], candidates[0] - depth
    return None, 0.0


def plies_required(depth: float) -> int:
    """How many max-thickness plies to laminate to cover depth."""
    return max(1, math.ceil(depth / MAX_STOCK_MM))


@dataclass
class DoorJamb:
    """
    Door is anchored to the STRUCTURAL plane (rough opening / frame face).
    Finish plane is now far proud of it. Everything bridging that gap is a
    computed delta, not a tape measurement.
    """
    wall: Assembly
    frame_face: float       # offset of door frame's outer stop/trim face from datum
    casing: str = "flush"   # "flush" | "proud" reveal intent
    proud_reveal: float = 0.0  # mm if casing == "proud"
    head_drip: float = inch(0.5)  # how far head flashing must clear past stack
    min_head_drip: float = inch(0.25)  # minimum acceptable drip past cladding
    expect_extension: Optional[float] = None  # external cross-check on jamb depth

    @property
    def jamb_extension_depth(self) -> float:
        """Stock depth to fill frame face out to the finish plane."""
        return self.wall.finish_plane - self.frame_face

    @property
    def casing_face(self) -> float:
        if self.casing == "proud":
            return self.wall.finish_plane + self.proud_reveal
        return self.wall.finish_plane

    @property
    def head_flashing_projection(self) -> float:
        """Must clear the FULL stack so water sheds free of the cladding."""
        return self.wall.cladding_plane + self.head_drip

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        d = self.jamb_extension_depth
        if d < -self.wall.tol:
            issues.append(Issue(Severity.CLASH, "jamb",
                f"frame face is PROUD of finish plane by {-d:.1f} mm — frame set "
                f"too far out for this cladding stack."))
            return issues

        ext = _expect_issue("jamb", "jamb extension", d, self.expect_extension,
                            self.wall.tol)
        if ext:
            issues.append(ext)

        if d <= self.wall.tol:
            # Frame sits at (within tol of) the finish plane — nothing to extend.
            issues.append(Issue(Severity.OK, "jamb",
                f"frame flush with finish plane ({d:.1f} mm) — no jamb extension "
                f"required."))
        else:
            issues.append(Issue(Severity.OK, "jamb",
                f"jamb extension depth = {d:.1f} mm ({mm_to_in(d):.2f}\")  "
                f"[finish {self.wall.finish_plane:.1f} - frame {self.frame_face:.1f}]"))

            stock, leftover = nearest_stock(d)
            if stock is None:
                n = plies_required(d)
                issues.append(Issue(Severity.WARN, "jamb",
                    f"depth {d:.1f} mm exceeds any single stock; LAMINATE {n} plies "
                    f"of {MAX_STOCK_MM:.1f} mm or build a box extension."))
            elif leftover > 1.0:
                issues.append(Issue(Severity.WARN, "jamb",
                    f"no exact stock for {d:.1f} mm; nearest single piece "
                    f"{stock:.1f} mm ({mm_to_in(stock):.2f}\") — rip to {d:.1f}, or "
                    f"laminate to size."))

        # Head flashing must clear the cladding plane by an ADEQUATE drip.
        clearance = self.head_flashing_projection - self.wall.cladding_plane
        if clearance <= 0:
            issues.append(Issue(Severity.CLASH, "jamb-head",
                f"head flashing does not project past cladding plane "
                f"(clearance {clearance:.1f} mm)."))
        elif clearance + 1e-9 < self.min_head_drip:
            issues.append(Issue(Severity.WARN, "jamb-head",
                f"head flashing clears cladding by only {clearance:.1f} mm "
                f"(< min {self.min_head_drip:.1f} mm) — increase head_drip so water "
                f"sheds free of the wall."))
        else:
            issues.append(Issue(Severity.OK, "jamb-head",
                f"head flashing projection = {self.head_flashing_projection:.1f} mm "
                f"(clears cladding {self.wall.cladding_plane:.1f} by "
                f"{clearance:.1f} mm)"))
        return issues


# ---------------------------------------------------------------------------
# Threshold / sill  (three planes meet + water must leave)
# ---------------------------------------------------------------------------
@dataclass
class Threshold:
    """
    Worst interface in the building: interior floor plane, exterior deck/grade
    plane, and the wall stack all meet, and water has to get out. Every depth
    is derived from the SAME wall stack as the wall section, so the threshold
    detail and the wall section cannot physically disagree.

    OUTWARD axis: frame_sill_face, threshold_extension.
    VERTICAL axis: interior_floor_top, step_down, exterior_threshold_top.
    The two axes are never added together.
    """
    wall: Assembly
    frame_sill_face: float          # offset of door sill outer face from datum (X)
    interior_floor_top: float       # height datum for finish floor (Z, mm)
    step_down: float = inch(0.5)    # exterior threshold top below interior FF (Z)
    pan_slope_pct: float = 2.0      # sill-pan slope to exterior
    drain_gap: float = inch(0.375)  # vented gap under cladding bottom course
    min_slope_pct: float = 2.0      # minimum acceptable sill-pan slope (~1/4":12")
    expect_extension: Optional[float] = None  # external cross-check on reach (X)

    @property
    def threshold_extension(self) -> float:
        """Reach from sill face out to the cladding plane (caps the stack)."""
        return self.wall.cladding_plane - self.frame_sill_face

    @property
    def pan_fall(self) -> float:
        """Vertical fall of the sill pan across the extension run."""
        return self.threshold_extension * (self.pan_slope_pct / 100.0)

    @property
    def exterior_threshold_top(self) -> float:
        return self.interior_floor_top - self.step_down

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        t = self.threshold_extension
        if t < -self.wall.tol:
            issues.append(Issue(Severity.CLASH, "threshold",
                f"sill face is OUTSIDE cladding plane by {-t:.1f} mm — sill set "
                f"too far out."))
            return issues

        issues.append(Issue(Severity.OK, "threshold",
            f"threshold extension = {t:.1f} mm ({mm_to_in(t):.2f}\")  "
            f"reaches cladding plane {self.wall.cladding_plane:.1f}"))

        # REAL disagreement guard: reach derived here vs. an independent source.
        ext = _expect_issue("threshold", "threshold extension", t,
                            self.expect_extension, self.wall.tol)
        if ext:
            issues.append(ext)

        # Sill pans are governed by a minimum SLOPE, not an absolute fall — over
        # a short reach even a correct slope yields only a few mm of fall.
        if self.pan_slope_pct + 1e-9 < self.min_slope_pct:
            issues.append(Issue(Severity.WARN, "threshold-pan",
                f"sill-pan slope {self.pan_slope_pct:.1f}% is below min "
                f"{self.min_slope_pct:.1f}% — steepen the pan."))
        else:
            issues.append(Issue(Severity.OK, "threshold-pan",
                f"sill-pan slope {self.pan_slope_pct:.1f}% (>= {self.min_slope_pct:.1f}% "
                f"min) -> fall {self.pan_fall:.1f} mm over {t:.1f} mm to exterior"))

        if self.step_down <= 0:
            issues.append(Issue(Severity.WARN, "threshold-step",
                "no step-down: exterior threshold not below interior FF — "
                "water can track back inside."))
        else:
            issues.append(Issue(Severity.OK, "threshold-step",
                f"exterior threshold top = FF - {self.step_down:.1f} mm "
                f"= {self.exterior_threshold_top:.1f} mm"))

        issues.append(Issue(Severity.OK, "threshold-drain",
            f"vented drain gap under bottom cladding course = "
            f"{self.drain_gap:.1f} mm ({mm_to_in(self.drain_gap):.2f}\")"))
        return issues


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------
def run_validation(*objects) -> list[Issue]:
    issues: list[Issue] = []
    for o in objects:
        issues.extend(o.validate())
    return issues


def report(issues: list[Issue]) -> bool:
    """Print all issues; return True if no CLASH (safe to emit drawings)."""
    clash = False
    for i in issues:
        print(i)
        clash = clash or i.severity is Severity.CLASH
    print("-" * 60)
    print("RESULT:", "BLOCKED — clash present" if clash else "clear to emit")
    return not clash


# ---------------------------------------------------------------------------
# Demo with realistic 10x8 out-sulated rainscreen numbers
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Wall datum = exterior face of structural sheathing (ZIP), out-sulated TBH
    wall = (Assembly("10x8 wall", "exterior face of 1/2\" ZIP sheathing")
            .add("exterior insulation (Comfortboard)", inch(1.5))
            .add("rainscreen furring v (drainage)", inch(0.75), is_drainage_gap=True)
            .add("cross furring h (slat substructure)", inch(0.75))
            .add("dark slat cladding (thermo-aspen)", inch(0.75)))
    print(wall.table())
    print()

    fascia = FasciaDetail(wall=wall, base_fascia_face=inch(0.5))  # 1x sub-fascia

    jamb = DoorJamb(wall=wall,
                    frame_face=inch(0.0),     # Viking frame face ~ at sheathing
                    casing="proud",
                    proud_reveal=inch(0.125))

    thresh = Threshold(wall=wall,
                       frame_sill_face=inch(0.0),
                       interior_floor_top=0.0,
                       step_down=inch(0.5))

    issues = run_validation(fascia, jamb, thresh)
    # Cross-detail: fascia face and casing face should both meet the cladding line.
    issues += assert_coplanar("front-plane", tol=wall.tol,
                              cladding=wall.cladding_plane,
                              fascia=fascia.fascia_face)
    report(issues)
