# Sauna Builder — Complete Build Blueprint

A complete, practical blueprint for designing and building a traditional Finnish
dry sauna. This repository takes you from an empty space (indoor room, garage
corner, or outdoor shed) to a finished, code-conscious, safe-to-use sauna.

> ⚠️ **Safety & code disclaimer.** This blueprint is a general engineering and
> construction guide, not a substitute for local building/electrical codes or a
> licensed professional. Heaters draw heavy current and saunas combine heat,
> moisture, and people — **always have electrical work inspected and pull the
> required permits.** See [`docs/09-safety-and-codes.md`](docs/09-safety-and-codes.md).

---

## What's in this blueprint

The build is documented in sequence. Read the docs in order the first time; use
them as a reference later.

| # | Document | What it covers |
|---|----------|----------------|
| 00 | [Overview & glossary](docs/00-overview.md) | How a sauna works, types, key terms |
| 01 | [Planning & site selection](docs/01-planning.md) | Indoor vs outdoor, location, budget |
| 02 | [Design & dimensions](docs/02-design-and-dimensions.md) | Sizing rooms, bench geometry, door |
| 03 | [Materials & bill of materials](docs/03-materials-bom.md) | Wood species, full BOM, quantities |
| 04 | [Framing & structure](docs/04-framing.md) | Studs, floor, ceiling, door rough opening |
| 05 | [Insulation & vapor barrier](docs/05-insulation-vapor-barrier.md) | R-values, foil barrier, sealing |
| 06 | [Heater selection & sizing](docs/06-heater-sizing.md) | kW calculation, electric vs wood |
| 07 | [Electrical](docs/07-electrical.md) | Circuits, wiring, lighting, controls |
| 08 | [Ventilation](docs/08-ventilation.md) | Intake/exhaust placement, airflow |
| 09 | [Safety & codes](docs/09-safety-and-codes.md) | Clearances, guards, GFCI, egress |
| 10 | [Interior finishing](docs/10-interior-finishing.md) | Paneling, benches, backrests, trim |
| 11 | [Build sequence & checklist](docs/11-build-sequence-checklist.md) | Step-by-step order of operations |
| 12 | [Maintenance & first fire](docs/12-maintenance.md) | Curing, cleaning, seasonal care |

Reference drawings live in [`blueprints/`](blueprints/):

- [`floor-plan.md`](blueprints/floor-plan.md) — plan-view layout (ASCII drawing)
- [`wall-section.md`](blueprints/wall-section.md) — wall build-up, layer by layer
- [`bench-detail.md`](blueprints/bench-detail.md) — bench framing & spacing
- [`wiring-diagram.md`](blueprints/wiring-diagram.md) — schematic for heater + light

---

## The reference build (at a glance)

This blueprint is anchored to one concrete example so every number is real. You
can scale it using the formulas in each doc.

- **Type:** Indoor electric dry sauna (Finnish style)
- **Interior size:** 6 ft × 5 ft × 7 ft high (≈ 1.83 × 1.52 × 2.13 m)
- **Capacity:** 3–4 adults
- **Volume:** ≈ 210 ft³ (≈ 5.9 m³)
- **Heater:** 6 kW electric, 240 V, dedicated 30 A circuit
- **Benches:** Two-tier; upper at 36 in, lower at 18 in
- **Wood:** Western Red Cedar paneling & benches; framing in kiln-dried SPF
- **Insulation:** R-13 walls, R-21 ceiling, foil vapor barrier throughout

See [`docs/02-design-and-dimensions.md`](docs/02-design-and-dimensions.md) for
how these numbers are derived and how to resize.

---

## Quick-start: the 12-step build

1. Finalize design & pull permits — [`01`](docs/01-planning.md), [`02`](docs/02-design-and-dimensions.md)
2. Order materials from the BOM — [`03`](docs/03-materials-bom.md)
3. Frame floor, walls, ceiling — [`04`](docs/04-framing.md)
4. Rough-in electrical & heater circuit — [`07`](docs/07-electrical.md)
5. Insulate cavities — [`05`](docs/05-insulation-vapor-barrier.md)
6. Install foil vapor barrier, sealed at all seams — [`05`](docs/05-insulation-vapor-barrier.md)
7. Install ventilation intake/exhaust — [`08`](docs/08-ventilation.md)
8. Panel ceiling, then walls (tongue-and-groove) — [`10`](docs/10-interior-finishing.md)
9. Build & mount benches and backrests — [`10`](docs/10-interior-finishing.md)
10. Mount heater, guard rail, controls; final electrical & inspection — [`06`](docs/06-heater-sizing.md), [`07`](docs/07-electrical.md), [`09`](docs/09-safety-and-codes.md)
11. Hang the door; install thermometer/hygrometer & accessories — [`10`](docs/10-interior-finishing.md)
12. Cure / first fire, then commission — [`12`](docs/12-maintenance.md)

Full detail in [`docs/11-build-sequence-checklist.md`](docs/11-build-sequence-checklist.md).

---

## Parametric detailing engine (code)

Alongside the written blueprint, the repo ships a small Python engine for
reconciling construction details of the **outdoor rainscreen-clad variant**,
where the envelope (out-sulation, drainage cavity, fascia/jamb/threshold) is the
hard part.

| File | Purpose |
|------|---------|
| [`planes.py`](planes.py) | Datum + layer-stack model. One datum per assembly; every interface is a derived delta off the same stack, so two details can't disagree. Clash/fit/coplanarity are real assertions. |
| [`sauna_engine.py`](sauna_engine.py) | Build orchestrator: defines the reference outdoor envelope, validates every interface, and — when clash-free — renders the drawing set. |
| [`drawing.py`](drawing.py) | Pure-Python SVG renderer. Draws scaled, dimensioned sheets straight from the validated planes (so drawings can't disagree with the model); rasterises to PDF if `cairosvg` is present. |
| [`tests/test_planes.py`](tests/test_planes.py) | Proves the guards actually catch disagreements (stale inputs, frame-proud, non-coplanar). |

```bash
python3 sauna_engine.py        # validate the envelope AND emit the drawing set
python3 planes.py              # the standalone detailing demo
python3 tests/test_planes.py   # run the test suite (no pytest needed)
```

The guarantee is enforced two ways: **single-sourcing** (every detail reads the
same `Assembly`) and **external cross-checks** (pass `expect=` from another
drawing/DXF and validation asserts the derived value matches). See the module
docstring in [`planes.py`](planes.py).

### Getting a printable blueprint set

`python3 sauna_engine.py` writes a numbered sheet set to [`drawings/`](drawings/)
**only if the model validates clash-free**:

| Sheet | Drawing |
|-------|---------|
| A-0 | Floor plan (room, benches, heater, vents, outswing door) |
| A-1 | Wall section (datum + dimensioned layer stack to the finish plane) |
| A-2 | Door jamb plan detail (frame face → jamb extension → casing) |
| A-3 | Threshold/sill section (reach, step-down, pan slope, drain gap) |

Outputs: one `.svg` + `.pdf` per sheet, a combined `sauna-blueprints.pdf`, and a
print-ready `index.html`.

- **No setup needed for SVG/HTML** — pure standard library.
- **PDF is optional:** `pip install -r requirements.txt` (cairosvg + pypdf). Without
  them you still get SVGs and `index.html`.
- **On iPhone:** open `index.html` (or any `.svg`) in Safari → Share → Print →
  pinch the preview → Save as PDF. Each sheet prints on its own page.

Every coordinate on every sheet is computed from the same derived planes the
engine validates — change a layer thickness and the report, the dimensions, and
the geometry all move together.

## How to use this repo

- Every doc is self-contained Markdown — read it on GitHub or in any editor.
- Numbers are given in both imperial and metric.
- Formulas are spelled out so you can recompute for your own room size.
- The [build checklist](docs/11-build-sequence-checklist.md) is meant to be
  printed and ticked off on site.

## License

Provided as-is for personal use. Verify all dimensions, loads, and electrical
specs against local code and manufacturer instructions before building.
