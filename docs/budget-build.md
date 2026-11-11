# Getting it under A$1,000

The full BOM is **A$2,250.28**. This is where that goes, what can come out, and
what each cut costs in speed. Prices as at 11 November 2026; the model's own
numbers come from `scripts/check_model.py` and `docs/design-notes.md`.

## First, two things that are already true

**The printed parts are already free.** Every bracket in the machine — motor
mounts, idler brackets, belt clamps, carriage bodies, Z nut mounts, the new Z
motor mount — is costed at zero in `bom.md`, under "Not costed here". Deciding
to print them saves nothing, because nothing was ever budgeted for them.

**The BOM is a buy-everything list.** It assumes you own none of it. That is
the right way to write a BOM and the wrong way to read a budget.

## Where the money actually goes

| Group | Cost | Share |
|---|---:|---:|
| Electronics | $552.28 | 24.5% |
| Linear motion — rails and carriage blocks | $488.25 | 21.7% |
| Frame, belts, fasteners | $480.50 | 21.4% |
| Hotends, extruders, fans | $449.90 | 20.0% |
| Motors | $139.80 | 6.2% |
| Bed stack | $139.55 | 6.2% |

No single group dominates, which is why there is no one thing to delete. But
the **top ten lines are half the total**:

| Line | Cost |
|---|---:|
| LDO Orbiter v2.5 extruder × 2 | $210.90 |
| MGN12H rail + carriage, 450 mm × 2 (Y) | $158.90 |
| MGN12H rail + carriage, 400 mm × 2 (Z) | $138.90 |
| BigTreeTech Octopus Pro V1.1 | $115.00 |
| Raspberry Pi 4 2 GB | $109.33 |
| Trianglelab V6 hotend × 2 | $90.00 |
| MGN12H carriage blocks × 5 | $90.00 |
| 4040 V-slot, 2.06 m | $90.00 |
| MGN12H rail + carriage, 500 mm (X) | $85.45 |
| TMC2209 drivers, 8-pack | $79.45 |

It is expensive because it is **all name brand, bought at Australian retail**:
LDO, Gates, Mean Well, Omron, Trianglelab, Raspberry Pi.

## What each cut costs in speed

The machine currently runs at **5,646 mm/s²**, set by the bed. The model is
`accel = f² × 2.21` and `f = (1/2π)√(k/m)`, calibrated on the two documented
points: the X toolhead at 506 g and 77.5 Hz, the bed at 1.34 kg and 50.6 Hz.
Those imply a chain stiffness of 120 and 135 kN/m respectively.

| Change | Saves | Machine runs at |
|---|---:|---:|
| Buy generic instead of brand | ~$434 | **5,646 mm/s²** — unchanged |
| Reuse your motors, bed and extruders | ~$580 | **5,646 mm/s²** — unchanged |
| One PSU instead of two | $69 | unchanged, but see below |
| **Rails → V-wheels** | ~$308 | **697 mm/s²** — 12% of it |

### Why V-wheels are the wrong saving

Calibrating on the Ender 3 — 0.40 kg at 32.5 Hz, the reference the whole model
was validated against — a V-wheel carriage chain is about **16.7 kN/m**, against
120–135 kN/m on rails. Eight times softer.

| On V-wheels | Frequency | Accel |
|---|---:|---:|
| X with the light Orbiter head (506 g) | 28.9 Hz | 1,845 mm/s² |
| X with the Titan head you own (667 g) | 25.2 Hz | 1,400 mm/s² |
| **Y, the bed (1.34 kg)** | **17.8 Hz** | **697 mm/s²** |

The bed is heavy, so it suffers most, and the slowest axis sets the machine.
You would pay $308 to turn a 5,646 mm/s² printer into an 697 mm/s² one — worse
than a stock Ender 3. **Every argument in this project for linear rails is an
argument against this cut.**

### Why the Orbiters are the right saving

Swapping the $105 Orbiters for the Titan and low-profile NEMA 17 you already
own adds about 160 g per toolhead. X drops from 13,259 to about 10,000 mm/s² —
and the machine does not slow down at all, because **X was never the limit**.
The bed is, at 5,646. You save $210.90 for nothing.

## The build that fits

| | Saving | Running total |
|---|---:|---:|
| **Full BOM** | | **$2,250.28** |
| *Reuse what you own* | | |
| Orbiter v2.5 × 2 → your Titan + low-profile NEMA 17 | $210.90 | |
| 4 of 5 bought NEMA 17s → motors you own (still buy the Z one) | $104.85 | |
| Bed, magnet and PEI → the 235 set off the old printer | $104.35 | |
| 4040 uprights and base rails → reuse the old frame | $90.00 | |
| Wiring, IEC inlet, drag chain → strip the old printer | $70.00 | $1,670.18 |
| *Swap, at verified local prices* | | |
| Pi 4 + 64 GB card + supply → Pi Zero 2 W ($34.20) + generic card | $134.53 | |
| TMC2209 8-pack → 5-pack ($49.45) plus one single ($11.45) | $18.55 | |
| Second 24 V supply → one 350 W, with the bed power-capped | $69.00 | $1,448.10 |
| *Buy generic instead of brand (estimated)* | | |
| 5 LDO rails → generic MGN12H, same geometry, looser tolerance | $208.25 | |
| Gates pulleys and idlers × 13 → generic GT2 | $72.65 | |
| Trianglelab V6 × 2 → generic V6 clones | $50.00 | |
| DREMC fans × 4 → generic 5015 and 4010 | $48.00 | |
| Gates 6 m belt → generic GT2 6 mm, 10 m | $41.00 | |
| Omron endstops × 4 → generic microswitches | $14.00 | **$1,014.20** |

**A$1,014 — 45% of the full BOM, at exactly the same 5,646 mm/s².**

Buying everything locally, with no overseas orders, lands at **A$1,448**.

## The three caveats

1. **The reuse column assumes what you own.** Two Titan extruders with
   low-profile NEMA 17s, four more NEMA 17s, the 235 × 235 bed with its magnet
   and PEI, and enough 4040 to rebuild the frame. If any of that is wrong, add
   it back. Full retail for all of it is $580.10.
2. **The generic column is estimated, not quoted.** Generic MGN12 rails are the
   one real risk: geometry is standard but tolerance and smoothness vary, and
   the rails are what the speed rests on. Buy one first and check it before
   committing to five.
3. **One PSU needs the bed power-capped.** The loads total 411.6 W against a
   350 W supply. Setting `max_power: 0.55` on the bed brings the total to 274 W
   (78%), which is inside the 80% rule `check_model.py` check 12 enforces. The
   cost is warm-up time: a 148 W bed instead of 270 W on a 255 × 245 plate.
   If you would rather not wait, the second supply is $69.

## What not to cut

- **The second carriage block per toolhead** ($18). It is worth +42% on X and
  is the cheapest performance in the whole machine.
- **The rails.** See above.
- **24 V.** On 12 V the motors run out of headroom at about 250 mm/s.
- **The Octopus Pro.** It is $115 for eight drivers; IDEX needs six, and the
  cheaper boards do not have them. The Manta M8P was already rejected because
  its CB1 module is unbuyable.
