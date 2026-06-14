# Wiring Diagram — Heater + Controls + Light (schematic)

> ⚠️ **Schematic only — for planning the layout, not for performing the work.**
> All electrical work must be done by a **licensed electrician**, sized to the
> heater nameplate and local code, and **inspected**. See
> [`../docs/07-electrical.md`](../docs/07-electrical.md).

## Reference: 6 kW electric heater, 240 V, dedicated circuit

```
  MAIN PANEL
  ┌─────────────────────────┐
  │  [≡] Double-pole breaker │  sized to heater nameplate (e.g. 30 A)
  │       + GFCI per code    │
  └───────────┬─────────────┘
              │  240 V feed (e.g. 10 AWG Cu — confirm w/ electrician)
              │
              ▼
        ┌───────────┐
        │ DISCONNECT │  (within sight / as required)
        └─────┬──────┘
              │
              ▼
     ┌──────────────────┐          ┌───────────────────────┐
     │  CONTROL UNIT     │◀────────▶│ TEMP SENSOR            │
     │  (digital, mounted│  sensor  │ high on wall, per      │
     │   OUTSIDE sauna)  │  cable   │ manufacturer spec      │
     └─────────┬─────────┘          └───────────────────────┘
               │  high-temp leads (inside hot room)
               ▼
        ┌─────────────┐
        │   HEATER     │  wall-mounted, all clearances met,
        │   (kiuas)    │  guard rail around it
        └─────────────┘

  LIGHTING (separate, switched outside)
  ┌──────────┐   ┌───────────────┐   ┌─────────────────────────┐
  │ supply   ├──▶│ switch OUTSIDE ├──▶│ sauna-rated light + guard│
  └──────────┘   └───────────────┘   └─────────────────────────┘
```

## Notes & requirements

| Item | Requirement |
|------|-------------|
| Circuit | **Dedicated** 240 V; nothing else shares it |
| Breaker | Double-pole, sized to **heater nameplate** + continuous-load rule |
| Wire | Gauge per nameplate, run length, temp rating, code (e.g. 10 AWG @ 30 A) |
| GFCI | Per local code |
| Disconnect | Provided as required, within sight |
| In-room wiring | **High-temp leads** only; junction boxes **outside** the hot room |
| Controller | Mounted **outside** (or heat-safe spot); enables timer/limit |
| Sensor | Placed **exactly** per manufacturer (high wall, set distance from ceiling/heater/vents) |
| Light | **Sauna-rated** fixture, guarded; **switch outside** |
| Barrier | Foil vapor barrier **sealed** around every penetration |
| Inspections | Rough-in **and** final, both passed |

## Sizing math (reference)

```
6000 W ÷ 240 V = 25 A nominal
25 A × 1.25 (continuous) = 31.25 A  → breaker/wire per nameplate & code
```

Different heater sizes: see the table in [`../docs/07-electrical.md`](../docs/07-electrical.md).
