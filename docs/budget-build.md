# Getting it under A$1,000

The full BOM is **A$2,235.38**. This is where that goes, what can come out, and
what each cut costs in speed. Australian prices as at 11 November 2026,
AliExpress as at 12 November 2026; the model's own numbers come from
`scripts/check_model.py` and `docs/design-notes.md`.

**Short answer: A$966**, buying overseas where it is cheaper and reusing what
you already own, at the same 5,646 mm/s2. Whether it lands under a thousand
comes down to one line — see "The one line that decides it".

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
| Buy overseas instead of local, same specification | $591.17 | **5,646 mm/s²** — unchanged |
| Reuse your motors, bed, frame and extruders | $504.19 | **5,646 mm/s²** — unchanged |
| One PSU instead of two | $69.00 | unchanged, but see below |
| **Rails → V-wheels** | ~$308 | **697 mm/s²** — 12% of it |

The first two rows are the whole budget: **$1,095 comes off without the machine
getting slower by a single mm/s²**, because neither touches stiffness or mass.
The fourth row is the one that does, and it is the one to refuse.

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

## What AliExpress actually costs

The first version of this page costed the generic column as "~$434, estimated".
That was my own figure and not a quote, which is exactly the thing this project
keeps catching itself doing. So every line was opened on AliExpress, in a
logged-out Australian session, with the right option selected on the listing
page, and the price read off it. The results are in `docs/bom.md` under the
**AliExpress** column, with the variant named and a `read as` tag saying how
firm each figure is.

Three things came out of that which change how the column should be read.

### Headline prices on AliExpress are not prices

A search result shows the *cheapest variant in the listing*. One result read
"MGN12H ... A$1.49". Opening it and selecting MGN12H at 500 mm gave A$38.01.
The $1.49 was a 100 mm MGN7 rail.

### There is a voucher under the sale price, and it does not repeat

Every cheap line showed exactly **A$1.49**. A 5 m belt: A$1.49. A 10 m belt from
the same listing: also A$1.49. That is a floor, not a price.

Solving the rail seller's three lengths pins it down. List 38.01 / 34.60 / 31.19
gave sale 10.75 / 8.26 / 5.77, and those fit `sale = 0.73 x list - 17.00`
exactly, across all three. So that seller was running a **27% discount** with a
flat **A$17.00 first-order voucher** on top, floored at A$1.49. The 27% repeats;
the $17 does not. Totalling the sale column would have understated the build by
several hundred dollars.

**So the BOM totals the list prices.** They are conservative, and the sale
prices are recorded beside them for reference.

### On branded parts the list price is a fake anchor

Two lines came out *dearer* overseas at list than at Australian retail:

| Line | Australia | AliExpress list | AliExpress sale |
|---|---:|---:|---:|
| Octopus Pro + 8 x TMC2209 | $194.45 | $211.22 | **$77.43** |
| Orbiter v2.5 x 2 | $210.90 | $338.94 | **$121.62** |

For commodity parts - rails, belt, pulleys, fans, bearings, endstops - the list
price is real and beats Australian retail by two to four times. For name-brand
parts the list price is an inflated anchor and only the sale price wins. The BOM
therefore never pays more overseas than at home: each line takes the cheaper of
the two.

## The build that fits

Order matters: take the overseas price first, then the local swaps, then
what you already own. Every row is generated from `docs/bom.json`, so the
running total cannot drift from the BOM.

| | Saving | Running total |
|---|---:|---:|
| **Full BOM, everything bought new at Australian retail** | | **$2235.38** |
| *Buy overseas wherever AliExpress list beats the local price* | | |
| 5 linear rails, 500 / 2 x 450 / 2 x 400 mm, generic MGN12H | $213.66 | |
| 13 pulleys and toothed idlers | $54.95 | |
| 2 lead screws, 500 mm, nut included | $52.34 | |
| Gates 6 m belt → 10 m of aramid GT2-6 | $49.81 | |
| 4 fans — 2 x 5015 blower, 2 x 4010 axial | $47.80 | |
| Bed plate, and one PEI sheet that brings its own magnet | $45.97 | |
| 2 V6 hotends, 24 V 50 W all-metal | $40.48 | |
| 5 NEMA 17s — a STEPPERONLINE 5-pack | $39.92 | |
| 5 extra MGN12H carriage blocks — the one gap no AU seller could fill | $23.75 | |
| 4 endstops, and a 10-pack of F688ZZ bearings | $22.49 | |
| | | **$1644.21** |
| *Swap for a cheaper local part* | | |
| Raspberry Pi 4 Model B, 2 GB → Pi Zero 2 W | $75.13 | |
| Official Raspberry Pi 64 GB A2 micro SD card → generic A2 card | $32.50 | |
| | | **$1536.58** |
| *Reuse what you already own* | | |
| 4040 V-slot black → reuse the old frame | $90.00 | |
| LDO NEMA 17 42STH48-2504AC → the two X motors you already own | $49.94 | |
| LDO Orbiter v2.5 extruder, motor included → the Titan + low-profile NEMA 17 you own | $210.90 | |
| LDO NEMA 17 42STH48-2504AC → the Y motor you already own | $24.97 | |
| Heated bed assembly, 255 x 245 mm, 24 V ~270 W → the 235 bed off the old printer | $28.99 | |
| Magnetic sheet 235 x 235, high-temp 3M adhesive → its magnet and PEI sheet too | $29.39 | |
| Wiring, ferrules, IEC inlet with switch and fuse, drag chain, sleeving → strip the old printer | $70.00 | |
| | | **$1032.39** |
| 10% GST, collected at checkout on the $425.09 of overseas lines | +$42.51 | **$1074.90** |

That is **$1,074.90** — just over. Which brings us to the line that decides it.

## The one line that decides it

The biggest single item left is the **Octopus Pro at $194.45**, bought locally,
because its AliExpress *list* price is dearer. But the same seller bundles the
board with eight TMC2209s, and on 12 November that bundle was **$77.43** - 4.9
stars over 54 ratings, 1,000+ sold.

| | Parts | GST | Total |
|---|---:|---:|---:|
| Budget build, everything at list prices | $1,032.39 | $42.51 | $1,074.90 |
| **...with the Octopus bundle at its sale price** | $915.37 | $50.25 | **$965.62** |
| ...with *every* line at the sale prices seen on 12 Nov | $654.13 | $24.13 | $678.26 |

**One line, $117, is the difference between over and under a thousand.** Watch
that listing and buy the board on a sale; everything else can be bought at list
and the budget still holds.

The $678 figure is real in the sense that it is what the basket rang up that
day, and unreal in the sense that it collects a first-order voucher on every
line when you only get it once. Do not plan on it. Plan on **$966**, and treat
anything below as a good day.

## What stays in Australia, and why

$607.30 of the budget build is still bought here. That is deliberate:

- **Both Mean Well supplies ($143.65).** Mains-side. A no-name 350 W supply
  behind a 270 W bed is not where to save $46. The HI-LINK LRS-350-24 lookalike
  is A$28.88 and it is tempting; it is still a lookalike.
- **The Octopus Pro**, unless it is on sale - see above.
- **Extrusion and the bed carrier bars ($143.20).** Cut-to-length metal. Heavy,
  slow and awkward to ship, and RM Components will cut it.
- **Fasteners, T-nuts and brackets ($91.25).** Small money, four weeks saved.
- **The Pi, the SD card, the Wago blocks and the ADXL345 ($72.75).** Cheaper or
  the same here; the ADXL345 is already A$4.95.

## The three caveats

1. **The reuse column assumes what you own.** Two Titan extruders with
   low-profile NEMA 17s, four more NEMA 17s, the 235 x 235 bed with its magnet
   and PEI, and enough 4040 to rebuild the frame. If any of that is wrong, add
   it back. Full retail for all of it is $575.15. Note the machine takes **four** NEMA 17s, not five — two on X, one on Y, one on Z, which drives both lead screws through a belt.
2. **The overseas column is quoted now, but it is not the same parts.** The
   rails are generic, not LDO - 4.7 stars over 130 reviews, and every reviewer
   says to degrease and re-grease them before use. The motors are 2.0 A
   STEPPERONLINE rather than 2.5 A LDO. The belt is not Gates. The lead screw
   comes with a plain brass nut, not the POM anti-backlash nut, so Z will have
   backlash unless you add one. The V6 listing has only nine reviews and one of
   them reports the wrong heater voltage in the box. **Buy one rail first and
   check it before committing to five** - the rails are what the speed rests on.
3. **The 255 x 245 bed has no overseas source.** No AliExpress seller had a
   heated bed that size at all. The 235 x 235 MK3 plate at A$28.99 costs you
   20 mm of `build_x` and 10 mm of `build_y`; the model will follow the
   parameters either way, but it is a smaller printer. The budget build dodges
   this by reusing the 235 bed off the old printer, which is the same size.

## What not to cut

- **The second carriage block per toolhead** ($18). It is worth +42% on X and
  is the cheapest performance in the whole machine.
- **The rails.** See above.
- **24 V.** On 12 V the motors run out of headroom at about 250 mm/s.
- **The Octopus Pro.** Eight drivers; IDEX needs six, and the cheaper boards do
  not have them. The Manta M8P was already rejected because its CB1 module is
  unbuyable. Buy it on sale, not instead.
- **The second 24 V supply** ($69). One 350 W supply forces `max_power: 0.55` on
  the bed to stay inside the 80% rule that `check_model.py` check 12 enforces,
  which means a 148 W bed warming a 255 x 245 plate. The loads total 411.6 W.
