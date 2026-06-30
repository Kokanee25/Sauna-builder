"""
drawing.py — render printable, dimensioned blueprint sheets from the engine.

Every coordinate on every sheet is computed from the SAME derived planes that
planes.py validates, so the drawings cannot disagree with the model. This is a
pure-stdlib SVG writer (no CAD/graphics deps). If `cairosvg` is importable, the
sheets are also rasterised to PDF; otherwise the SVG (and the print index.html)
open in any browser / on a phone and print to PDF from there.

Convention matches planes.py: +X = OUTWARD from the datum (mm).
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional

from planes import mm_to_in, Assembly, DoorJamb, Threshold, FasciaDetail


# ---------------------------------------------------------------------------
# Minimal SVG sheet builder with architectural dimension lines
# ---------------------------------------------------------------------------
INK = "#1a1a1a"
THIN = "#9aa0a6"
ACCENT = "#b03a2e"
PAPER = "#ffffff"


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


@dataclass
class Sheet:
    title: str
    number: str            # e.g. "A-1"
    subtitle: str = ""
    w: int = 1100
    h: int = 850
    scale_note: str = "NOT TO SCALE — do not measure print; use figured dims"

    def __post_init__(self) -> None:
        self._b: list[str] = []

    # --- primitives ---------------------------------------------------------
    def line(self, x1, y1, x2, y2, stroke=INK, width=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._b.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                       f'y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{d}/>')

    def rect(self, x, y, w, h, fill="none", stroke=INK, width=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                       f'height="{h:.1f}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{width}"{d}/>')

    def text(self, x, y, s, size=13, anchor="start", fill=INK, weight="normal",
             rotate: Optional[float] = None):
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
        self._b.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                       f'font-family="Helvetica,Arial,sans-serif" '
                       f'text-anchor="{anchor}" fill="{fill}" '
                       f'font-weight="{weight}"{tr}>{_esc(s)}</text>')

    def poly(self, pts, fill="none", stroke=INK, width=1.4, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._b.append(f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{width}"{d}/>')

    def arc(self, cx, cy, r, x1, y1, x2, y2, stroke=THIN, width=1.0, dash="4 3"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._b.append(f'<path d="M {x1:.1f} {y1:.1f} A {r:.1f} {r:.1f} 0 0 1 '
                       f'{x2:.1f} {y2:.1f}" fill="none" stroke="{stroke}" '
                       f'stroke-width="{width}"{d}/>')

    def _tick(self, x, y, vertical=False):
        # 45° architectural tick
        s = 5
        if vertical:
            self.line(x - s, y - s, x + s, y + s, stroke=INK, width=1.2)
        else:
            self.line(x - s, y + s, x + s, y - s, stroke=INK, width=1.2)

    # --- dimension lines ----------------------------------------------------
    def dim_h(self, x1, x2, y, label, size=12):
        self.line(x1, y, x2, y, stroke=INK, width=1.0)
        self._tick(x1, y); self._tick(x2, y)
        self.text((x1 + x2) / 2, y - 6, label, size=size, anchor="middle")

    def dim_v(self, y1, y2, x, label, size=12):
        self.line(x, y1, x, y2, stroke=INK, width=1.0)
        self._tick(x, y1, vertical=True); self._tick(x, y2, vertical=True)
        self.text(x + 6, (y1 + y2) / 2 + 4, label, size=size, anchor="start")

    def witness(self, x, y1, y2):  # thin extension line
        self.line(x, y1, x, y2, stroke=THIN, width=0.8)

    # --- assemble -----------------------------------------------------------
    def svg(self) -> str:
        body = "\n".join(self._b)
        tb_y = self.h - 70
        title_block = (
            f'<line x1="40" y1="{tb_y}" x2="{self.w-40}" y2="{tb_y}" '
            f'stroke="{INK}" stroke-width="1.4"/>'
            f'<text x="40" y="{tb_y+24}" font-size="18" font-family="Helvetica,Arial" '
            f'font-weight="bold" fill="{INK}">{_esc(self.title)}</text>'
            f'<text x="40" y="{tb_y+42}" font-size="12" font-family="Helvetica,Arial" '
            f'fill="{THIN}">{_esc(self.subtitle)}</text>'
            f'<text x="{self.w-40}" y="{tb_y+24}" font-size="18" '
            f'font-family="Helvetica,Arial" font-weight="bold" text-anchor="end" '
            f'fill="{ACCENT}">{_esc(self.number)}</text>'
            f'<text x="{self.w-40}" y="{tb_y+42}" font-size="11" '
            f'font-family="Helvetica,Arial" text-anchor="end" fill="{THIN}">'
            f'{_esc(self.scale_note)} · generated by sauna_engine</text>'
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
            f'height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
            f'<rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>'
            f'<rect x="20" y="20" width="{self.w-40}" height="{self.h-40}" '
            f'fill="none" stroke="{INK}" stroke-width="2"/>'
            f'{body}{title_block}</svg>'
        )


def _dual(mm: float) -> str:
    return f'{mm:.0f} mm ({mm_to_in(mm):.2f}")'


# ---------------------------------------------------------------------------
# Sheet A-1 : Wall section (the layer stack, dimensioned off the datum)
# ---------------------------------------------------------------------------
LAYER_FILL = ["#f6e7bf", "#eef4f7", "#e3cf9c", "#d4ab74", "#cd966a", "#c98a5a"]


def wall_section(wall: Assembly, number="A-1") -> Sheet:
    sh = Sheet("WALL SECTION — outdoor rainscreen envelope", number,
               subtitle=f"datum: {wall.datum_desc}   ·   horizontal = OUTWARD from datum")
    scale = 5.2  # px per mm
    x0, ytop, H = 150.0, 120.0, 360.0
    # datum
    sh.line(x0, ytop - 24, x0, ytop + H + 90, stroke=ACCENT, width=1.4, dash="6 4")
    sh.text(x0, ytop - 30, "DATUM = 0", size=12, anchor="middle", fill=ACCENT,
            weight="bold")
    run = 0.0
    fi = 0
    for ly in wall.layers:
        x = x0 + run * scale
        wpx = ly.thickness * scale
        fill = LAYER_FILL[fi % len(LAYER_FILL)]
        if ly.is_drainage_gap:
            sh.rect(x, ytop, wpx, H, fill="#eef4f7", stroke=THIN, dash="3 3")
            sh.text(x + wpx / 2, ytop + H / 2, "VENT", size=10, anchor="middle",
                    fill=THIN, rotate=-90)
        else:
            sh.rect(x, ytop, wpx, H, fill=fill, stroke=INK)
        # leader label
        ly_in = mm_to_in(ly.thickness)
        sh.text(x + wpx / 2, ytop - 8,
                f"{ly.thickness:.0f}", size=11, anchor="middle")
        sh.text(x + wpx / 2, ytop + H + 22, ly.name, size=10.5, anchor="end",
                rotate=-35)
        run += ly.thickness
        fi += 1
    x_fin = x0 + run * scale
    # finish/cladding plane
    sh.line(x_fin, ytop - 24, x_fin, ytop + H + 90, stroke=ACCENT, width=2.0)
    sh.text(x_fin + 8, ytop - 18, "FINISH / CLADDING PLANE", size=12, fill=ACCENT,
            weight="bold")
    sh.text(x_fin + 8, ytop - 2, _dual(wall.finish_plane), size=11, fill=ACCENT)
    # cumulative running dimension under the stack
    dy = ytop + H + 70
    runc = 0.0
    for ly in wall.layers:
        x1 = x0 + runc * scale
        runc += ly.thickness
        x2 = x0 + runc * scale
        sh.dim_h(x1, x2, dy, f"{ly.thickness:.0f}")
    # overall
    sh.dim_h(x0, x_fin, dy + 36, f"OVERALL  {_dual(wall.finish_plane)}")
    # interior / exterior callouts
    sh.text(x0 - 12, ytop + H / 2, "STRUCTURE →", size=12, anchor="end")
    sh.text(x_fin + 8, ytop + H / 2 + 18, "← WEATHER", size=12)
    return sh


# ---------------------------------------------------------------------------
# Sheet A-2 : Door jamb plan detail
# ---------------------------------------------------------------------------
def jamb_plan(jamb: DoorJamb, number="A-2") -> Sheet:
    w = jamb.wall
    sh = Sheet("DOOR JAMB — plan detail", number,
               subtitle="frame anchored to structure; jamb extension bridges to finish plane")
    scale = 5.2
    x0, ytop, H = 230.0, 140.0, 300.0
    # frame block (interior side, left of datum)
    fx = x0 + jamb.frame_face * scale
    sh.rect(fx - 130, ytop, 130, H, fill="#dfe6ea", stroke=INK)
    sh.text(fx - 65, ytop + H / 2, "DOOR FRAME", size=12, anchor="middle")
    sh.line(fx, ytop - 20, fx, ytop + H + 80, stroke=INK, width=1.2, dash="6 4")
    sh.text(fx, ytop - 26, "frame face", size=11, anchor="middle")
    # wall stack (datum at x0)
    run = 0.0
    fi = 0
    for ly in w.layers:
        x = x0 + run * scale
        wpx = ly.thickness * scale
        if ly.is_drainage_gap:
            sh.rect(x, ytop, wpx, H, fill="#eef4f7", stroke=THIN, dash="3 3")
        else:
            sh.rect(x, ytop, wpx, H, fill=LAYER_FILL[fi % len(LAYER_FILL)],
                    stroke=INK)
        run += ly.thickness
        fi += 1
    x_fin = x0 + w.finish_plane * scale
    sh.line(x_fin, ytop - 20, x_fin, ytop + H + 80, stroke=ACCENT, width=2.0)
    sh.text(x_fin + 6, ytop - 26, "finish plane", size=11, fill=ACCENT)
    # jamb extension hatch (frame face -> finish plane)
    sh.rect(fx, ytop + H / 2 - 16, x_fin - fx, 32, fill="#f2d9b0", stroke=INK)
    sh.text((fx + x_fin) / 2, ytop + H / 2 + 5, "JAMB EXTENSION", size=11,
            anchor="middle")
    # casing
    cx = x0 + jamb.casing_face * scale
    if jamb.casing == "proud":
        sh.rect(x_fin, ytop + 30, cx - x_fin, H - 60, fill="#caa06a", stroke=INK)
        sh.text(cx + 6, ytop + 26, f"casing PROUD {_dual(jamb.proud_reveal)}",
                size=10.5, fill=INK)
    # dimensions
    dy = ytop + H + 54
    sh.dim_h(fx, x_fin, dy, f"jamb extension  {_dual(jamb.jamb_extension_depth)}")
    # head-flashing note
    sh.text(x0, ytop + H + 96,
            f"HEAD FLASHING must project to {_dual(jamb.head_flashing_projection)} "
            f"(clears cladding by {_dual(jamb.head_drip)})", size=11, fill=ACCENT)
    return sh


# ---------------------------------------------------------------------------
# Sheet A-3 : Threshold / sill section
# ---------------------------------------------------------------------------
def threshold_section(th: Threshold, number="A-3") -> Sheet:
    w = th.wall
    sh = Sheet("THRESHOLD / SILL — section detail", number,
               subtitle="three planes meet; pan slopes out, step-down keeps water outside")
    scale = 5.2
    x0, ff_y = 240.0, 230.0   # x0 = datum; ff_y = interior finish-floor line
    # interior floor
    sh.line(x0 - 200, ff_y, x0, ff_y, stroke=INK, width=2.0)
    sh.text(x0 - 196, ff_y - 8, "INTERIOR FINISH FLOOR (FF)", size=11)
    # sill pan sloping out to cladding plane
    sx = x0 + th.frame_sill_face * scale
    cx = x0 + w.cladding_plane * scale
    fall_px = th.pan_fall * scale * 2.0  # exaggerate Z a touch for legibility
    sh.poly([(sx, ff_y + 12), (cx, ff_y + 12 + fall_px)], stroke=ACCENT, width=2.4)
    sh.text((sx + cx) / 2, ff_y + 28 + fall_px,
            f"SILL PAN  slope {th.pan_slope_pct:.1f}%  (fall {th.pan_fall:.0f} mm)",
            size=10.5, anchor="middle", fill=ACCENT)
    # exterior threshold top (stepped down)
    ext_y = ff_y + th.step_down * scale * 2.0
    sh.line(cx, ext_y + 12 + fall_px, cx + 150, ext_y + 12 + fall_px,
            stroke=INK, width=2.0)
    sh.text(cx + 80, ext_y + 6 + fall_px, "EXTERIOR THRESHOLD / DECK", size=11,
            anchor="middle")
    # wall stack above, from cladding plane inward (schematic)
    sh.rect(sx, ff_y - 150, cx - sx, 150, fill="#f2d9b0", stroke=INK)
    sh.text((sx + cx) / 2, ff_y - 150 / 2, "WALL STACK ABOVE", size=11,
            anchor="middle")
    sh.line(cx, ff_y - 165, cx, ext_y + 40, stroke=ACCENT, width=2.0)
    sh.text(cx + 6, ff_y - 158, "cladding plane", size=11, fill=ACCENT)
    sh.line(sx, ff_y - 165, sx, ff_y + 30, stroke=INK, width=1.2, dash="6 4")
    sh.text(sx, ff_y - 170, "sill face", size=11, anchor="middle")
    # dims
    sh.dim_h(sx, cx, ff_y - 185, f"threshold reach  {_dual(th.threshold_extension)}")
    sh.dim_v(ff_y, ext_y, x0 - 60, f"step-down {_dual(th.step_down)}")
    # drain gap note
    sh.text(x0 - 200, ff_y + 120,
            f"Vented drain gap under bottom cladding course: {_dual(th.drain_gap)}",
            size=11, fill=INK)
    return sh


# ---------------------------------------------------------------------------
# Sheet A-0 : Floor plan
# ---------------------------------------------------------------------------
@dataclass
class Room:
    """Interior plan of the sauna (mm). Plan is drawn from these figures."""
    name: str
    width: float        # X (mm)
    depth: float        # Y (mm)
    height: float       # ceiling (mm) — shown as a note
    bench_upper_depth: float
    bench_lower_depth: float
    door_width: float
    heater_w: float = 400.0
    heater_d: float = 250.0


def floor_plan(room: Room, number="A-0") -> Sheet:
    sh = Sheet(f"FLOOR PLAN — {room.name}", number,
               subtitle=f"interior {room.width:.0f} x {room.depth:.0f} mm  ·  "
                        f"ceiling {room.height:.0f} mm  ·  plan view")
    # fit room into a box
    avail_w, avail_h = 720.0, 470.0
    scale = min(avail_w / room.width, avail_h / room.depth)
    ox, oy = 220.0, 150.0
    W, D = room.width * scale, room.depth * scale
    # room
    sh.rect(ox, oy, W, D, fill="#fbf7ef", stroke=INK, width=2.0)
    # benches on the back (top) wall
    bu = room.bench_upper_depth * scale
    bl = room.bench_lower_depth * scale
    sh.rect(ox, oy, W, bu, fill="#e3cf9c", stroke=INK)
    sh.text(ox + W / 2, oy + bu / 2 + 4, "UPPER BENCH (36\")", size=11,
            anchor="middle")
    sh.rect(ox, oy + bu, W, bl, fill="#efe1c0", stroke=INK)
    sh.text(ox + W / 2, oy + bu + bl / 2 + 4, "LOWER BENCH (18\")", size=11,
            anchor="middle")
    # heater near the door wall (bottom-right)
    hw, hd = room.heater_w * scale, room.heater_d * scale
    hx, hy = ox + W - hw - 10, oy + D - hd - 10
    sh.rect(hx, hy, hw, hd, fill="#cd966a", stroke=INK)
    sh.text(hx + hw / 2, hy + hd / 2 + 4, "HEATER", size=10.5, anchor="middle")
    # intake vent (low, under/near heater) + exhaust (opposite, low)
    sh.rect(hx + hw / 2 - 8, oy + D - 6, 16, 6, fill=ACCENT, stroke=INK)
    sh.text(hx + hw / 2, oy + D + 18, "intake", size=10, anchor="middle",
            fill=ACCENT)
    sh.rect(ox - 6, oy + D - 60, 6, 16, fill=ACCENT, stroke=INK)
    sh.text(ox - 10, oy + D - 64, "exhaust", size=10, anchor="end", fill=ACCENT)
    # airflow arrow (diagonal sweep)
    sh.poly([(hx + hw / 2, oy + D - 18), (ox + 30, oy + D - 44)],
            stroke=THIN, width=1.2, dash="5 4")
    # door on bottom wall with outswing arc
    dwid = room.door_width * scale
    dx = ox + 30
    dy = oy + D
    sh.line(dx, dy, dx + dwid, dy, stroke=PAPER, width=4.0)  # break the wall
    sh.line(dx, dy, dx, dy + dwid, stroke=INK, width=2.0)     # leaf swinging out
    sh.arc(dx, dy, dwid, dx + dwid, dy, dx, dy + dwid)
    sh.text(dx + dwid + 6, dy + dwid, "DOOR (outswing, 24\")", size=10.5)
    # dimensions
    sh.dim_h(ox, ox + W, oy - 24, _dual(room.width))
    sh.dim_v(oy, oy + D, ox - 40, _dual(room.depth))
    return sh


# ---------------------------------------------------------------------------
# Output: write SVGs, optional PDFs, and a print-ready index.html
# ---------------------------------------------------------------------------
def save_set(sheets: list[Sheet], outdir: str) -> dict:
    os.makedirs(outdir, exist_ok=True)
    written = {"svg": [], "pdf": []}
    try:
        import cairosvg  # type: ignore
        have_pdf = True
    except Exception:
        have_pdf = False

    for sh in sheets:
        svg = sh.svg()
        base = f"{sh.number}_{sh.title.split(' — ')[0].strip().lower().replace(' ', '-').replace('/', '-')}"
        svg_path = os.path.join(outdir, base + ".svg")
        with open(svg_path, "w") as f:
            f.write(svg)
        written["svg"].append(svg_path)
        if have_pdf:
            pdf_path = os.path.join(outdir, base + ".pdf")
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=pdf_path)
            written["pdf"].append(pdf_path)

    # combined PDF if possible
    if have_pdf and written["pdf"]:
        _try_merge_pdf(written["pdf"], os.path.join(outdir, "sauna-blueprints.pdf"))

    _write_index(sheets, outdir)
    return written


def _try_merge_pdf(pdfs: list[str], out: str) -> None:
    try:
        from pypdf import PdfWriter  # type: ignore
    except Exception:
        return
    w = PdfWriter()
    for p in pdfs:
        w.append(p)
    with open(out, "wb") as f:
        w.write(f)


def _write_index(sheets: list[Sheet], outdir: str) -> None:
    cards = []
    for sh in sheets:
        base = f"{sh.number}_{sh.title.split(' — ')[0].strip().lower().replace(' ', '-').replace('/', '-')}"
        cards.append(
            f'<section class="sheet"><h2>{_esc(sh.number)} · {_esc(sh.title)}</h2>'
            f'<img src="{base}.svg" alt="{_esc(sh.title)}"/></section>')
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<title>Sauna Blueprints</title>"
        "<style>"
        "body{font-family:Helvetica,Arial,sans-serif;margin:24px;color:#1a1a1a}"
        "h1{margin:0 0 4px}p.tip{color:#666;margin:0 0 20px}"
        ".sheet{margin:0 0 28px}.sheet img{width:100%;max-width:1100px;"
        "border:1px solid #ddd}"
        "@media print{.sheet{page-break-after:always}p.tip{display:none}}"
        "</style>"
        "<h1>Sauna Build — Blueprint Set</h1>"
        "<p class='tip'>On iPhone: Share → Print → pinch the preview to save as PDF. "
        "Each sheet prints on its own page.</p>"
        + "".join(cards))
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(html)
