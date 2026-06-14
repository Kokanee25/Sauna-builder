# 02 — Design & Dimensions

This page turns "how many people" into actual numbers you can build to.

## 1. Sizing by capacity

Rule of thumb: allow **~6 ft² (0.56 m²) of floor per person seated**, and enough
bench length for everyone to sit (and ideally for one person to lie down).

| Capacity | Suggested interior footprint | Floor area |
|----------|------------------------------|------------|
| 2 people | 4 × 4 ft (1.2 × 1.2 m) | 16 ft² |
| 3–4 people | **6 × 5 ft (1.83 × 1.52 m)** ← reference | 30 ft² |
| 4–6 people | 6 × 7 ft (1.83 × 2.13 m) | 42 ft² |
| 6–8 people | 8 × 8 ft (2.44 × 2.44 m) | 64 ft² |

**Ceiling height: 7 ft (2.1 m).** This is the single most important dimension —
keep it low. The upper bench should sit in the hottest air, and a low ceiling
keeps that hot layer right where people are.

> **Why low ceilings?** Heat stratifies. A 7 ft ceiling means the hot band is at
> head height when seated on the upper bench. An 8–9 ft ceiling pushes the heat
> above the bathers and wastes heater capacity.

## 2. The reference build

```
Interior:    6 ft (W) × 5 ft (D) × 7 ft (H)
             1.83 m   × 1.52 m   × 2.13 m
Volume:      210 ft³  (5.95 m³)
Capacity:    3–4 adults
```

This 210 ft³ volume drives heater sizing (≈ 6 kW — see
[`docs/06-heater-sizing.md`](06-heater-sizing.md)).

## 3. Bench geometry

Benches are the heart of the layout. Standard tiered design:

| Bench | Height above floor | Depth | Notes |
|-------|--------------------|-------|-------|
| **Upper** | 36 in (915 mm) | 24 in (610 mm) | Hottest; deep enough to sit cross-legged or lie down |
| **Lower** | 18 in (460 mm) | 18 in (460 mm) | Cooler; also a step up to the upper bench |
| **Foot / step** | (floor) | — | Optional low step in front of lower bench |

Key clearances:

- **Headroom above upper bench:** at least **44 in (1.12 m)** of clear space from
  the upper bench seat to the ceiling, so a seated adult isn't cramped.
  With a 7 ft (84 in) ceiling and a 36 in upper bench, you get 48 in — good.
- **Gap between upper bench and wall behind:** leave a small gap (¾–1 in) or use a
  backrest so the back doesn't touch hot paneling.
- **Bench-to-heater clearance:** keep benches and bodies out of the heater's
  required clearance zone (see [`docs/06`](06-heater-sizing.md) / [`09`](09-safety-and-codes.md)).

Detailed framing in [`blueprints/bench-detail.md`](../blueprints/bench-detail.md).

### Bench length

Allow **~24 in (610 mm) of seat width per seated person**. The reference upper
bench runs the full 6 ft (72 in) wall → comfortably seats 3, or one person lies
down. The lower bench runs the same wall for seating and access.

## 4. Door

- **Size:** Standard sauna door is **24 in (610 mm) wide × 78–80 in tall**.
  Narrower than a normal door to reduce heat loss; the rough opening is sized to
  the door unit you buy.
- **Swing:** **OUTWARD, always.** Never lockable from outside. This is a safety
  requirement, not a preference. See [`docs/09`](09-safety-and-codes.md).
- **Glass:** Tempered glass doors are popular and safe; full-glass fronts look
  great but add cost and slightly reduce insulation — bump heater size if you use
  lots of glass.
- **Threshold:** Low or no threshold; a small gap under the door (≈ ¾ in / 19 mm)
  doubles as part of the ventilation path.

## 5. Layout principles (plan view)

- Put the **heater near the door wall**, with its **fresh-air intake low and
  near/under the heater**.
- Put **benches on the wall opposite or perpendicular to the door**, away from
  the heater's swing-room.
- Put the **exhaust vent low on the wall opposite the heater** (diagonal airflow
  across the room). More in [`docs/08-ventilation.md`](08-ventilation.md).
- Keep the **walking path** clear from door to benches.

See the plan-view drawing in [`blueprints/floor-plan.md`](../blueprints/floor-plan.md).

## 6. Resizing for your space — the formulas

If your room isn't 6×5×7, recompute:

1. **Volume (ft³)** = width × depth × height (all in ft).
2. **Heater kW** ≈ volume ÷ 35 for a well-insulated electric sauna (round up to
   the next available heater; add capacity for glass/masonry/log walls). Full
   method in [`docs/06`](06-heater-sizing.md).
3. **Bench length** = 24 in × (people seated at once).
4. **Upper-bench headroom** = ceiling height − upper-bench height ≥ 44 in.

Worked example (reference): 6 × 5 × 7 = 210 ft³ → 210 ÷ 35 = 6 kW. ✅

Next: [`03 — Materials & bill of materials`](03-materials-bom.md)
