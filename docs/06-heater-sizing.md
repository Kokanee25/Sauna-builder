# 06 — Heater Selection & Sizing

The heater (kiuas) is the single most important component. Size it to the room,
not the other way around.

## 1. Sizing rule

For a **well-insulated electric Finnish sauna**:

> **Heater kW ≈ interior volume (ft³) ÷ 35**
> (metric: **kW ≈ volume (m³) × 1.0–1.5**, i.e. roughly 1 kW per m³)

Then **round up** to the nearest available heater size, and **add capacity** for
heat-loss factors below.

### Reference build

```
Volume = 6 × 5 × 7 = 210 ft³  (5.95 m³)
210 ÷ 35 = 6.0 kW   →  choose a 6 kW heater ✅
```

### Add capacity for heat loss

Add to your raw estimate (bump up a heater size) if you have:

| Factor | Extra |
|--------|-------|
| Large glass door / glass wall | + ~1 kW per ~2 m² of glass |
| Uninsulated log or masonry walls | + significant (treat each m² of such wall as extra volume — see manufacturer) |
| Exposed exterior wall in cold climate | + a margin |
| High ceiling (>7 ft) | + (more air to heat) |

A typical heater-maker chart phrases this as "add X m³ equivalent per m² of glass
or uninsulated wall." Follow the **specific heater's manual** — it overrides this
rule of thumb.

## 2. Don't oversize or undersize

- **Undersized:** never reaches temperature, runs constantly, stones don't get hot
  enough for good löyly.
- **Oversized:** heats the air fast but **doesn't store enough heat in the
  stones**, and can short-cycle; löyly is weak and the room feels harsh. Match the
  heater to the room.

## 3. Electric heater types

| Type | Description | Notes |
|------|-------------|-------|
| **Wall-mounted** | Hangs on a wall, compact | Most common for small/medium saunas (reference build) |
| **Floor-standing** | Larger stone capacity | Better löyly, needs floor space + clearance |
| **Integrated control** | Knobs/timer on the unit | Simple, cheaper |
| **Separate digital control** | Wall panel outside or inside | Scheduling, precise temp, often required for larger units |

For the reference 6 kW build: a **wall-mounted 6 kW heater** with a digital
controller is the sweet spot.

## 4. Stones

- Use **only heater-rated igneous stones** (peridotite/olivine-diabase). They
  withstand thermal shock from water. Never use random rocks (they can crack or
  explode).
- **Rinse** stones before first use to remove dust.
- **Stack loosely** around and between elements so air circulates — do not pack
  tight. Follow the heater's stone weight spec (≈ 40–50 lb / 18–22 kg typical for
  a 6 kW unit).
- **Re-stack** stones annually; replace crumbled ones (see [`docs/12`](12-maintenance.md)).

## 5. Clearances (critical safety)

Every heater has **minimum clearances** to walls, benches, ceiling, and floor —
**follow the heater's manual exactly.** General guidance:

- Maintain the stated gap from heater sides/front to walls, benches, and any
  combustible surface.
- Install the **wooden guard rail** around the heater so bathers can't touch the
  hot body or fall onto it.
- Keep benches and the bather zone **outside** the clearance envelope.
- Mount at the manufacturer's height above the floor.

More on guards/clearances: [`docs/09-safety-and-codes.md`](09-safety-and-codes.md).

## 6. Wood-burning option (outdoor)

If you choose a wood stove instead of electric:

- Size by the maker's **m³ rating** for the firebox.
- Requires a **listed chimney** with correct clearances, a **floor heat
  shield/hearth**, wall shields, a **spark arrestor**, and **combustion air**.
- Often needs solid-fuel-appliance approval/inspection. See [`docs/09`](09-safety-and-codes.md).
- No electrical circuit for the heater itself (you may still wire lighting).

## 7. Heater checklist

- [ ] kW computed from volume (÷35 imperial) and rounded up
- [ ] Capacity added for glass/uninsulated/cold-wall factors
- [ ] Heater model selected; **its manual obtained and read**
- [ ] Stone type and weight confirmed per manual
- [ ] Required clearances mapped onto the floor plan
- [ ] Guard rail planned
- [ ] Electrical requirements handed to electrician → [`docs/07`](07-electrical.md)

Next: [`07 — Electrical`](07-electrical.md)
