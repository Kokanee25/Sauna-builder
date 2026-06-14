# 00 — Overview & Glossary

## How a sauna works

A traditional (Finnish) sauna is a small, very well-insulated room heated to
**150–195 °F (65–90 °C)** with **low humidity**. A heater (electric element or
wood stove) heats a pile of stones; ladling water on the stones produces a
short burst of steam called **löyly**, briefly raising humidity and the
*felt* temperature without making the room permanently wet.

Three things make a sauna a sauna rather than just a hot room:

1. **Heat retention** — heavy insulation + a reflective vapor barrier keep heat
   in and protect the structure from moisture.
2. **Stratification** — hot air rises, so benches are stacked; you choose your
   temperature by choosing your bench height.
3. **Controlled air exchange** — fresh-air intake near the heater and an exhaust
   on the opposite side keep oxygen up and circulate heat without bleeding it
   all away.

## Sauna types

| Type | Heat source | Humidity | Notes |
|------|-------------|----------|-------|
| **Finnish / dry** | Electric or wood stove + stones | Low, with löyly bursts | The classic; this blueprint targets it |
| **Steam room** | Steam generator | ~100% | Different build (tile, full waterproofing) — not covered here |
| **Infrared** | IR emitters (no stones) | None | Lower temps (~120–140 °F), simpler wiring, not a true sauna |
| **Smoke (savusauna)** | Wood, no chimney | Low | Traditional, advanced; out of scope |

This blueprint covers the **Finnish dry sauna**, with notes for **electric** and
**wood-burning** heaters.

## Electric vs. wood-burning heater

| | Electric | Wood-burning |
|---|----------|--------------|
| Best for | Indoor, urban, convenience | Outdoor, off-grid, ambiance |
| Install | Dedicated 240 V circuit | Chimney + floor/wall heat shields |
| Heat-up | 30–45 min, thermostat control | 45–60 min, manual tending |
| Code burden | Electrical permit, GFCI | Chimney clearances, hearth, combustion air |
| Running cost | Electricity | Firewood |

See [`docs/06-heater-sizing.md`](06-heater-sizing.md).

## Anatomy of the wall (outside → inside)

```
exterior wall / room  →  studs + insulation  →  foil vapor barrier
   →  air gap (furring, optional)  →  tongue-and-groove cedar paneling  →  sauna interior
```

Each layer is detailed in [`docs/05-insulation-vapor-barrier.md`](05-insulation-vapor-barrier.md)
and drawn in [`blueprints/wall-section.md`](../blueprints/wall-section.md).

## Glossary

- **Löyly** (LOO-loo) — the steam/heat burst from ladling water on the stones;
  also the general "feel" of the sauna's heat.
- **Kiuas** (KEE-oo-as) — the sauna heater/stove.
- **Vapor barrier** — foil (usually foil-faced kraft or pure aluminum foil)
  applied to the warm/interior side of insulation to block moisture and reflect
  radiant heat back into the room.
- **Tongue-and-groove (T&G)** — interlocking paneling boards; the standard
  sauna interior surface.
- **Stratification** — vertical temperature layering; the basis for tiered benches.
- **Clear / knot-free** — wood grade with no knots (knots get hot and bleed
  sap); preferred for benches and backrests you touch.
- **Duckboard** — removable slatted floor mat for drainage and comfort underfoot.
- **Foot clearance** — gap below the lower bench so feet/air can move and the
  floor can dry.

Next: [`01 — Planning & site selection`](01-planning.md)
