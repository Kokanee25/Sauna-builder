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

## How to use this repo

- Every doc is self-contained Markdown — read it on GitHub or in any editor.
- Numbers are given in both imperial and metric.
- Formulas are spelled out so you can recompute for your own room size.
- The [build checklist](docs/11-build-sequence-checklist.md) is meant to be
  printed and ticked off on site.

## License

Provided as-is for personal use. Verify all dimensions, loads, and electrical
specs against local code and manufacturer instructions before building.
