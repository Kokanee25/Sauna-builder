# 07 — Electrical

> ⚠️ **Hire a licensed electrician and get it inspected.** A sauna heater is a
> large 240 V load in a hot, occasionally damp room. This page tells you what to
> plan and ask for — it is **not** a substitute for code or a pro. Codes (NEC in
> the US, CEC in Canada, others elsewhere) and local rules govern the final work.

## 1. The heater circuit

A 6 kW heater is a **dedicated 240 V circuit** — it cannot share with anything.

### Sizing the circuit (worked example)

```
Heater: 6 kW @ 240 V
Current = Power / Voltage = 6000 W / 240 V = 25 A
Continuous-load rule (×1.25): 25 A × 1.25 = 31.25 A
→ Breaker: 30 A is too small at 1.25×; size per actual nameplate.
```

Heater nameplates and local code drive the final breaker/wire. Common pairings:

| Heater | Nominal current @240 V | Typical breaker | Typical copper wire* |
|--------|------------------------|-----------------|----------------------|
| 4.5 kW | ~19 A | 30 A | 10 AWG |
| **6 kW** | **~25 A** | **30 A** | **10 AWG** |
| 8 kW | ~33 A | 40–50 A | 8 AWG |
| 9 kW | ~37.5 A | 50 A | 8 AWG |

\* Wire gauge depends on length, temperature rating, insulation type, and code —
**confirm with your electrician.** The heater manual specifies minimum wire and
breaker; follow it.

### Key requirements

- **Dedicated double-pole breaker** sized to the heater's nameplate.
- **GFCI protection** as required by local code for the circuit.
- **Disconnect** within sight / as required, so the heater can be isolated.
- **High-temperature wiring** for any cable inside the hot room (heater whip,
  sensor) — standard NM/Romex is not rated for in-sauna heat; use the heater's
  specified high-temp leads and route per the manual.
- **Junction boxes outside the hot room** where possible.
- Wiring that passes the foil vapor barrier must be **sealed** at the foil
  (see [`docs/05`](05-insulation-vapor-barrier.md)).

## 2. The control unit

Two arrangements:

1. **Integrated controls** on the heater body — simplest; you operate it inside.
2. **Separate digital controller** — mounted **outside** the sauna (common) or in
   a heat-safe spot inside, with a **temperature sensor** placed high on a wall
   per the manual. Enables timers, scheduling, and remote start.

The temperature **sensor location is specified by the manufacturer** (usually
high on the wall, a set distance from the ceiling and away from the heater and
vents). Place it exactly as instructed or the heater will mis-read the room.

## 3. Lighting

- Use a **sauna-rated, heat- and moisture-resistant fixture** (vapor-tight,
  rated for the temperature). Standard fixtures will fail or become a hazard.
- Mount it **lower on a wall or under a bench**, shielded by a wooden light guard,
  not on the hot ceiling — both for fixture life and to avoid glare. Many builds
  use a fixture at upper-wall height behind a guard, or LED strip rated for
  saunas.
- **Low-voltage / LED sauna lighting** is popular and runs cooler.
- Switch is mounted **outside** the sauna.
- Lighting may be on its own small circuit or fed appropriately — per electrician.

## 4. What NOT to put in the hot room

- No standard receptacles/outlets inside the hot room.
- No thermostats/switches rated only for normal rooms.
- No speakers/electronics unless specifically sauna-rated.
- No standard light fixtures or ceiling-mounted lights over the heater.

## 5. Rough-in vs. finish

- **Rough-in** (before insulation/paneling): run the heater feed to its location,
  the sensor cable, and the light cable; set boxes; leave service loops.
- **Inspection #1:** many jurisdictions inspect rough wiring before you cover it.
- **Finish** (after paneling): mount heater, connect leads, mount controller and
  sensor, install light + guard.
- **Inspection #2 / final:** before commissioning.

## 6. Electrical checklist

- [ ] Licensed electrician engaged; permit pulled
- [ ] Dedicated 240 V circuit sized to heater nameplate
- [ ] Correct breaker + wire gauge (per manual & code)
- [ ] GFCI protection per local code
- [ ] Disconnect provided as required
- [ ] High-temp leads used inside the hot room; junctions kept outside
- [ ] Controller mounted; sensor placed exactly per manual
- [ ] Sauna-rated light + guard; switch outside
- [ ] Foil barrier sealed around every wire penetration
- [ ] Rough-in and final inspections passed

Next: [`08 — Ventilation`](08-ventilation.md)
