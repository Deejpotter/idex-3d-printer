# Design notes

Engineering findings for the IDEX printer, in the order they were established.
Figures that have been checked are stated plainly; figures that have not are
marked. Several earlier conclusions in this project turned out to be wrong and
the corrections are kept here rather than quietly deleted.

## 1. What actually limits the speed

Stiffnesses in series: the floppiest link sets the answer.

```
1/k_total = 1/k_belt + 1/k_mount + 1/k_gantry
f = (1/2pi) * sqrt(k/m)
accel [mm/s2] ~= f^2 * 2.21
```

| Link | Stiffness | Note |
|---|---|---|
| GT2 6 mm belt, both spans | 513 kN/m | |
| Toolhead on ONE MGN12H block | 141 kN/m | the limiting link on the original design |
| Toolhead on TWO MGN12H blocks | 282 kN/m | |
| 2040 gantry beam at 480 mm | 478 kN/m | scales as 1/L^3 |
| 2040 gantry beam at 520 mm | 376 kN/m | the cost of longer carriages |

Result:

| Machine | Moving mass | f | Accel |
|---|---|---|---|
| Original: 1 block, 1.42 kg toolhead | 1.42 kg | 40.0 Hz | 3,541 mm/s² |
| This design: 2 blocks, 518 g toolhead | 0.518 kg | 77.5 Hz | 13,259 mm/s² |
| Y axis (the bed) | 1.27 kg | 51.9 Hz | **5,948 mm/s²** |

**The bed is still the slowest axis.** `max_accel` in `printer.cfg` is set to
5,900 for that reason. Raising it further means stiffening the bed again.

See §12 for how the bed got from 4,255 to 5,948 mm/s², and for the correction
to the stiffness figure that made the earlier number wrong.

Motor torque is not the constraint: an LDO 42STH48-2504AC at 0.45 N·m holding,
derated to 60% at speed, pushes about 42 N through a 20-tooth GT2 pulley, which
is 82,000 mm/s² on the toolhead and 23,000 mm/s² on the bed. Both are far above
the structural limits.

## 2. A correction: blind-bolting into extrusion ends is NOT weak

An earlier version of this analysis claimed the upright-to-base joint was the
speed limiter and that corner brackets were worth +51%. That was wrong, and the
error was a single-bolt model applied to a four-bolt joint.

A preloaded bolted butt joint is effectively rigid until the applied moment
overcomes the clamp force and the faces separate. Four M5 bolts at ±10 mm,
preloaded to a conservative 2.5 kN each, resist about **130 N·m**. The moment
this machine actually applies at an upright foot is about **3 N·m** — a factor
of forty inside the limit.

| Upright foot | Pair stiffness | Gain |
|---|---|---|
| 4 blind bolts, as drawn | 478 kN/m | — |
| Plus a gusset on the loaded face | 636 kN/m | +5% |
| Plus gussets on both faces | 670 kN/m | +6% |
| A perfectly rigid welded foot | 724 kN/m | +7% |

Even replacing the foot with a weld buys 7%. The joint is fine.

**But the rule is not universal.** Measured off the real profiles:

| Profile | Section area | Tapped bores |
|---|---|---|
| 40 × 40 V-slot | 458.46 mm² | **four**, Ø4.6, at (±10, ±10) |
| 20 × 40 V-slot | 299.99 mm² | two, Ø4.2, at (0, ±10) |
| 20 × 20 V-slot | 171.40 mm² | **one**, Ø4.2, dead centre |

The 2020 has a single central bore — that genuinely is the weak single-bolt case.
**Corner-bracket the 2020 ends; don't bother on the 4040 uprights.**

## 3. The one real defect at the feet is screw length

Thread engagement for M5 into 6063 aluminium through a 2.2 mm wall:

| Screw | Engagement | Verdict |
|---|---|---|
| M5 × 8 | 5.8 mm | too short — below 2 × diameter |
| M5 × 12 | 9.8 mm | marginal |
| **M5 × 16** | 13.8 mm | correct |

Preload is the entire reason a blind joint is stiff, so too little thread turns a
good joint into the floppy one the wrong analysis described. Use M5 × 16 at the feet.

## 4. Where the two carriage blocks go

Two arrangements were considered. The toolhead's centre of mass sits about 40 mm
forward of the rail; accelerating along X at that offset makes a moment about Z.

- **Blocks separated along X** resist that moment directly with a force couple.
- **Blocks separated along Z** (two rails on the beam) cannot make a couple about
  Z at all, so they do not help the dominant mode.

So the blocks go in line along X. The cost is beam length — the carriage grows to
100 mm and the beam with it:

| Arrangement | Beam | k_total | Accel | Gain |
|---|---|---|---|---|
| 1 block, 480 mm beam | 480 | 89.8 | 4,411 | — |
| 2 blocks in line, 520 mm beam | 520 | 122.6 | 6,021 | +37% |
| 2 blocks in line, 560 mm beam | 560 | 113.4 | 5,569 | +26% |

(Those accelerations are for a 1.14 kg toolhead, the figure used while choosing
the arrangement. The built toolhead is lighter, which is why §1 is higher.)

The beam-lengthening penalty is real: at 560 mm, a third of the gain is given
back. `end_allow` was trimmed from 50 to 30 mm to hold the beam at 520.

## 5. The gantry height is set by the toolhead

`gantry_z = bed_top + th_drop`, where `th_drop` (75 mm) is the distance from the
X beam underside to the nozzle tip.

Before the toolhead existed as geometry, the gantry sat at a placeholder height of
`base_h + 60` = 100 mm. Modelling the real toolhead put the **nozzle 68 mm below
the top of the bed**. It is now driven by the parameter instead of guessed.

This is the clearest argument for modelling before buying.

## 6. Corrections to earlier figures

| Claim | Was | Is | Why |
|---|---|---|---|
| Frame mass | 12.985 kg | **4.484 kg** | every component had inherited Fusion's default Steel; density was 7850 instead of 2700 |
| Layout jig mass | 143.8 kg | **18 g** | the hidden parametric skeleton was steel blocks; it now carries a 1 kg/m³ material |
| Upright foot joint | +51% available | **+7%** | single-bolt model applied to a four-bolt joint, see §2 |
| Second MGN12H block | "about $8" | $8 on AliExpress, **$105 at Australian retail** | the gain is real; the price was not a local one |
| Assembly occurrence count | 77 | 294 | 77 was the Frame's child count quoted as the whole |
| Fastener count | 140 | 153 | |

Verification of the mass correction: the 2020 member computes 0.463 kg/m against
OpenBuilds' published 0.47 kg/m, and the 4040 upright at 500 mm computes 618.9 g
(458.46 mm² × 500 mm × 2.7 g/cm³ = 618.9 g).

## 7. What the model is, and what it is not

**Is:**
- 38 driving parameters; lengths *and* positions follow them, held by rigid joints
  to a grounded layout skeleton.
- Real V-slot cross-sections, traced from the actual profiles and re-drawn
  natively, within 0.003 mm² of the originals.
- Real hub parts for the lead screws, anti-backlash nut blocks and the Z motor.
- Verified by flexing: `upright_h` at 620, 440 and back to 500 moves the top tie
  to 660–680, 480–500, 540–560 with the envelope tracking and a clean timeline.

**Is not:**
- Fastener-complete. The frame carries one screw assortment line, not 153 parts.
- Printed-part complete. Motor mounts, idler brackets, belt clamps and the Z nut
  mounts do not exist yet.
- Free of simplifications. Interference analysis reports **4 overlaps of exactly
  4320 mm³**, which is the simplified carriage blocks passing through the rails
  they would really wrap. That is deliberate. Any *other* interference is a fault.
- Mass-accurate from CAD alone. Imported STEP has no iron, copper or magnets in
  it: the NEMA 17's own geometry computes 520 g against a real 390 g. Simplified
  and imported parts therefore carry a per-part density chosen to hit the
  datasheet mass. The frame, rails and plates use real materials.

## 8. Fusion API notes, for anyone scripting this

- `root.allOccurrences` gives world-space positions. `occurrence.component.occurrences`
  does not, and reading bounding boxes from the latter silently returns stale or
  local coordinates.
- A metal appearance is coloured by **`metal_f0`**, not `surface_albedo`. Setting
  `surface_albedo` renders the whole frame as a black silhouette.
- `occurrence.transform2` can only be set on a proxy obtained from the root
  component (`createForAssemblyContext`), and in a parametric design the change
  must be committed with `snapshots.add()` *before* any `computeAll()`, or it is
  silently discarded.
- `addTwoPointRectangle` via the API adds **zero** geometric constraints, unlike
  the UI. Sketches need explicit horizontal/vertical constraints to be fully
  defined.
- A script that raises an exception has **all** of its changes rolled back,
  including parameters added earlier in the same script.
- A rigid joint between two planar faces picks its own rotation about the face
  normal. On a non-square profile it lands 90° out; set `JointInput.angle`
  explicitly and search 0/90/180/270.
- `occurrences.addExistingComponent(component, matrix)` applies the matrix
  **relative to the previous occurrence of that component**, so a list of
  placements accumulates. Add at identity and set `transform2` afterwards.
- `snapshots.add()` silently reverts the transform of some referenced
  occurrences — it did for every NEMA 17 while leaving the pulleys alone. The
  fix is to wrap the part in a native component and transform the wrapper.
- A sketch on `xZConstructionPlane` has its second axis along **−Z**, so a
  feature placed at +z lands at −z and cuts nothing. The failed cut leaves an
  unhealthy "No target body!" feature in the timeline.

## 9. Commissioning — before the first print

Nothing in `klipper/printer.cfg` has run on hardware. In order:

1. Flash the Manta M8P V2.0 for STM32H723, 128 KiB bootloader, 25 MHz crystal.
2. Replace the `[mcu] serial:` path with the real one from `ls /dev/serial/by-id/*`.
3. Check every motor direction one axis at a time with `FORCE_MOVE`, before homing.
4. Verify each endstop with `QUERY_ENDSTOPS` before allowing a homing move.
5. Confirm the two carriages cannot collide: `safe_distance: 110` assumes 110 mm
   carriage plates. Measure yours.
6. `PID_CALIBRATE` both hotends and the bed. The values in the config are
   placeholders copied from the reference config.
7. Calibrate `rotation_distance` on both extruders. 4.637 is the Orbiter nominal.
8. Measure the T0→T1 offsets with a calibration print and set them in `T1`.
9. `SHAPER_CALIBRATE` each toolhead. The model predicts ~77 Hz on X and ~42 Hz on
   Y. If the measured numbers are far off, the machine is not built as drawn —
   find out why before raising `max_accel`.

## 10. What the completed model added

Everything in the machine is now modelled: X motors, idlers, belts and mounts;
the Y rails, blocks, bed carrier, heated bed, motor, idler and belt; the Z belt
link, screw bearing blocks and motor; and the electronics bay behind the frame.

| Sub-assembly | Parts | Mass |
|---|---:|---:|
| A — Frame | 7 | 3,684 g |
| B — X gantry | 16 | 1,745 g |
| C — Toolhead A | 6 | 518 g |
| C — Toolhead B | 6 | 518 g |
| D — Y and bed | 17 | 3,811 g |
| E — Z axis | 26 | 1,921 g |
| G — Electronics | 2 | 2,291 g |
| **Total** | **80 bodies** | **14.51 kg** |

Overall envelope with motors and the electronics bay: 556 × 583 × 598 mm.

Real parts inserted from the hub: both lead screws, both anti-backlash nut
blocks, four NEMA 17 motors, six GT2 pulleys, five GT2 idlers and four 688ZZ
bearings. Everything else is native geometry.

**No clean free STEP exists for three parts.** The MGN12H carriage block, the
Orbiter v2.5 and the V6 are all modelled as simplified solids carrying a
density chosen to hit the datasheet mass:

- The hub's own MGN12H models are **1,027 and 1,186 bodies** — every ball
  modelled. Unusable in an assembly that needs ten of them. Both the rail and
  the block are instead drawn from the HIWIN MGN12 datasheet: a 14-point rail
  section with ball grooves and top chamfers, and a proper C-section block.
  The rail section computes **0.694 kg/m** against HIWIN's published ~0.72,
  which is the check that the profile is right.
- Searching turned up only paid marketplace STEP or community redraws of
  uncertain provenance for all three. A wrong STEP is worse than an honest
  simplified solid with the right envelope and the right mass.

### Interference after completion

Seven overlaps remain, and every one is a shaft or belt meeting a part that
would carry a bore in reality:

| Count | Volume | What |
|---:|---:|---|
| 2 | 992 mm³ | lead screw through its pulley — **see below** |
| 1 | 384 mm³ | Z motor shaft through its pulley |
| 4 | 70–122 mm³ | belt runs tangent to pulleys and idlers |

The four 4,320 mm³ rail/block overlaps are gone: the carriage blocks are now
modelled as the C-section they actually are, so they wrap the rail instead of
passing through it.

Fifteen others were fixed: the X motor pulleys fouled their own mount plates,
both X idlers and the Y idler fouled their brackets, and the Z screw bearing
blocks had no bore. All now corrected.

**The lead screw / pulley overlap is a real finding, not a simplification.**
The hub pulley has a **6.35 mm bore** and the TR8 screw is **8 mm**. The BOM
already specifies an 8 mm bore pulley for the screws; the model is using the
wrong master because that is what the hub holds. Buy the 8 mm bore part.

## 12. Design changes after review

### The bed was over-built, and the first fix would have made it worse

The bed was a **6 mm 235 × 235 carrier plate** (895 g) carrying a **6 mm heated
bed** (1,060 g). Both were guesses. The real Creality part is **3 mm**.

The obvious move — delete the carrier, drop the bed to 3 mm — is wrong, and the
numbers say why. Carrier stiffness computed from geometry, `k = 48EI/L³` over
the 200 mm rail spacing:

| Carrier | k | Moving mass | k_total | f | Accel |
|---|---:|---:|---:|---:|---:|
| 235 × 6 plate + 6 mm bed (original) | 1,751 kN/m | 2,169 g | 164.8 | 43.9 Hz | 4,255 |
| 2 bars 40 × 3 | 293 kN/m | 1,199 g | 112.3 | 48.7 Hz | 5,243 |
| **2 bars 35 × 5** | **521 kN/m** | **1,269 g** | **134.9** | **51.9 Hz** | **5,948** |
| 2 bars 30 × 6 | 666 kN/m | 1,275 g | 142.9 | 53.3 Hz | 6,273 |
| full 235 × 3 plate | 438 kN/m | 1,494 g | 128.5 | 46.7 Hz | 4,815 |

Two thin 3 mm bars are **six times floppier** than the plate they replace. The
mass saving still wins, but far less than it looks. Stiffness goes as t³, so
going from 3 mm to 5 mm bars costs 70 g and buys 78% more carrier stiffness.

**35 × 5 bars it is**, at 111 g each. The bed stack is now carrier bars (5) +
silicone levelling spacers (2.5) + aluminium bed with bonded heater (3) +
magnetic sheet (1) + PEI spring steel (0.5), which keeps `bed_top` at exactly
93 mm so nothing else in the machine moves.

**Correction:** the 3,219 mm/s² quoted earlier used an *assumed* 400 kN/m for
the carrier. Computing it from the actual plate geometry gives 1,751 kN/m and
4,255 mm/s² for the original bed. The real gain from this change is
**4,255 → 5,948, +40%** — not the +85% that comparing against the old wrong
number would suggest.

### Board changed: Manta M8P → Octopus Pro

The Manta M8P needs a CB1 or CM4 compute module in its socket, and **no
Australian supplier stocks the CB1**. That made the single most important part
of the BOM unbuyable.

| | Manta M8P v2.0 | **Octopus Pro V1.1** |
|---|---|---|
| Board | $145 | **$115, in stock** |
| Host | CB1 not stocked; CM4 ~$76 | any Raspberry Pi over USB, ~$85 |
| Driver slots | 8 | 8 |
| MCU | STM32H723 | STM32H723 |
| Total | ~$221, blocked | **~$200, all in stock** |

Cheaper, in stock, and the separate Pi is easier to replace or debug. It also
solves the accelerometer: the Octopus Pro has no ADXL header, but the Pi's own
SPI does the job, which the Manta route would have needed anyway.

`printer.cfg` is rewritten against
[BigTreeTech's Octopus Pro reference config](https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/blob/master/Firmware/Klipper/generic-bigtreetech-octopus-pro-v1.1.cfg).
One departure, flagged in the file: BTT writes Driver3's `enable_pin` without
the leading `!` where every other driver has one. TMC2209 enable is active low,
so it is inverted here — check the motor actually enables before trusting it.

### Considered and rejected

- **Sherpa Mini + pancake motor** ($92/head) instead of the Orbiter ($105/head).
  Saves $27 across two heads and is perhaps 20 g lighter each, but flow is
  lower and it is a kit to assemble rather than a finished unit. Published
  weights for both disagree wildly between sources — anywhere from 95 to 148 g
  — so the weight argument is not solid enough to act on.
- **CR-6 SE bed kit** (255 × 245, $55.95, in stock) instead of the 235 × 235
  that is out of stock. It would give a slightly larger build area for $6 more,
  but it changes `build_x` and `build_y`, and those do not yet propagate
  downstream (§13). Worth revisiting once they do.

## 13. The parametric claim only covers the frame

Measured, not assumed. Driving `build_x` and `build_y` to 300 mm:

| Part | Follows? |
|---|---|
| X beam, uprights, base, top tie, bed rails | **yes** |
| X rail, carriage blocks, toolheads, hotends | no |
| Y rails, bed carrier, heated bed | no |
| Lead screws, Z plates, Z rails | no |
| Electronics | no |

The frame grows correctly and everything mounted to it stays where it was.
The reason is simple: the frame members are rigid-jointed to a parametric
layout skeleton, while everything added afterwards is placed at a fixed
transform.

What *does* propagate correctly is the vertical stack: `bed_top` is built from
the real layer thicknesses, and `gantry_z = bed_top + th_drop`, so changing the
bed construction moves the gantry to match. That is why the bed rebuild above
kept `bed_top` at 93 mm deliberately — so the beam would not move away from
toolheads that cannot follow it.

**Do not treat this model as parametric beyond the frame** until every
sub-assembly is jointed to the layout the way the frame members are.

## 14. The mounting audit

Interference checking says no two parts share space. It says nothing about
whether they can be **bolted together**. Measuring where the V-slots actually
are, by probing the traced profiles point by point:

| Interface | Slot centres | Rail centre | Verdict |
|---|---:|---:|---|
| Z rails on the 4040 upright face | 10.0 and 30.0 | 20.0 | **could not be bolted** |
| X rail on the 2040 beam face | 178.0 and 198.0 | 188.0 | **could not be bolted** |
| Y rails on the 2020 bed rails | 160.0 | 160.0 | correct |
| Upright feet into the base rail | 10.0 and 30.0 | 10.0, 30.0 | correct |
| Z motor onto the top tie underside | 255.0 and 275.0 | 238.0 | misses both |

A 2020 face has **one** slot, dead centre. A 40 mm face has **two**, at ±10 from
centre, with nothing between them. Centring a 12 mm rail on a 40 mm face — which
is what looks right — puts it exactly where there is no slot. The Y rails were
fine only because they happen to sit on 2020.

Both rails have been moved onto the measured slot centres (x 30/490, z 198), and
the carriage blocks and belt A with them.

### Twelve brackets float

Asking whether each bracket touches any frame member at all:

| Bracket | Clearance to nearest frame member |
|---|---:|
| X motor mounts (2) | 20 mm |
| X idler brackets (2) | 18 mm |
| Y motor mount | 46 mm |
| Y idler bracket | 8 mm |
| Z screw blocks (4) | 6 mm |
| PSU and control board | 2 mm |

Every one is hanging in space. They were placed to be in the right *place* and
nothing checked they could be *attached*. They are placeholders for printed
parts that do not exist yet, but the model should not pretend otherwise.

## 15. Can the heated bed bolt to the carriages? No.

6061 grows 23.6 µm/m/K. From 20 °C to 100 °C:

| Span | Growth |
|---|---:|
| Between the two rail centres (200 mm) | **0.378 mm** |
| Between the two carrier bars (105 mm) | 0.198 mm |
| Across the full bed (235 mm) | 0.444 mm |

The bed plate's axial stiffness is `EA/L` = 243 kN/mm, so holding back 0.378 mm
takes **92 kN**. Nothing survives that — the plate bows or the carriages are
destroyed. An MGN12 carriage is a preloaded ball bearing with microns of
clearance; it has no business absorbing a third of a millimetre.

**So the bed is never bolted to the blocks.** The stack is bed → silicone
spacers → carrier bars → blocks, and the spacers are the compliant element.
Each takes half the growth, 0.189 mm of shear. An M3 through a 4.5 mm clearance
hole gives 0.75 mm of float per side, which is ample.

### What the audit did find

The two carrier bars were **independent** — nothing tied them together in Y,
which is the driving direction, except the bed sitting on compliant spacers.
Pull on the belt and the pair racks. Added: a **spine between the bars making an
H-frame** (66 g) and a **belt clamp on the spine** (9 g), so belt load goes into
a closed structure rather than through a silicone puck.

Moving bed mass is now 1,344 g, up from 1,269 g for the spine and clamp.

## 16. Where every remaining dimension came from

| Part | Source | What it gave |
|---|---|---|
| **Orbiter v2.5** | **measured from a real STEP** — the A4T Orbiter extruder adapter, Armchair Heavy Industries, GitHub | 2 × M3 clearance Ø3.4 at **37.0 mm centres** (x −17.50 and +19.50, both y 0), filament bore Ø4.4 at the origin |
| E3D V6 | RepRap wiki groove-mount convention | Ø16 boss, **Ø12 groove × 4.64 wide**, heatsink Ø22.3 × 26 |
| NEMA 17 | NEMA standard | 42.3 square, **31.0 × 31.0** bolt pattern, Ø22 pilot boss |
| MGN12 / MGN12H | HIWIN datasheet | rail 12 × 8 on 25 pitch; block 27 × 45.4 × 13, M3 on 20 × 20 |
| 5015 blower | SOFASCO sDB5015 drawing | 51.5 × 51.5 × 15, 2 × Ø4.0 |
| Octopus Pro | BTT publish an official STEP — **24 MB, 113,000 points** | rejected; board drawn at its published 160 × 100 |
| Mean Well LRS-350-24 | Mean Well datasheet | 215 × 115 × 30 |

No vendor publishes the Orbiter's hole pattern and no official CAD exists. But the
A4T toolhead ships a 203 KB STEP of its *Orbiter adapter*, and an adapter is
nothing but the interface. Importing it and reading the cylinder axes gave the
pattern exactly — and it is **asymmetric**, 17.5 mm one side of the filament bore
and 19.5 mm the other.

The Octopus STEP is worth recording as a negative result: official, correct, and
**unusable** at 24 MB for a part that contributes an outline and four holes. That
is the trap §rule 3 was written for.

## 17. Every bracket now lands on a slot

| Bracket | Was | Bolts to |
|---|---:|---|
| X motor mounts (2) | 20 mm clear | beam top / underside, slot y = 216 |
| X idler brackets (2) | 18 mm clear | beam top / underside, slot y = 216 |
| Y motor mount | 46 mm clear | base cross front face, slots z = 10 and 30 |
| Y idler bracket | 8 mm clear | base cross back face, slots z = 10 and 30 |
| Z screw blocks (4) | 6 mm clear | upright and base rail inner faces |
| PSU and control board | 2 mm clear | a new electronics panel, itself bolted to the base cross |

Each is an L-bracket: a foot lying flat on a frame face over a measured slot, a
web, and a plate carrying the part. The webs are **split either side of the
pulleys** they reach past — the first attempt drove a solid web straight through
the X pulleys and idlers.

Landing them created six new clashes at once: both motor mounts through their own
pulleys, both idler brackets through their idlers, the Y motor through its own
plate, and the rebuilt Z screw blocks losing the bores they had. All found by
measurement. **Interference is back to seven**, all the original
shaft-or-belt-through-bore class, and **zero brackets float**.

### Two bugs worth recording

- `'Y motor mount'` also starts with `'Y motor'`. A prefix match meant to move the
  motor moved the mount too, translating a part already in absolute coordinates by
  a further (260, 480, 42) and parking it 480 mm outside the machine. Caught by
  rendering, not by any check — which is an argument for always looking at the
  picture as well as the numbers.
- A float test that keyed frame members by name collapsed the two uprights into
  one, so a bracket correctly touching the left upright read as 126 mm from "the"
  upright. The test was wrong, not the model.

## 18. A more reliable way than looking at it

Every fault in this project was found by measuring, and every one that got in
was placed by eye. Screenshots do not tell you whether a rail is centred on a
slot, whether a bracket touches anything, or whether a parameter reaches the
part it is meant to drive.

`scripts/check_model.py` asserts the design rules instead. Run it as a Fusion
script with the assembly open. Current result:

```
PASS  nozzle A at bed_top                   nozzle z=93.00  bed_top=93.00
PASS  nozzle B at bed_top                   nozzle z=93.00  bed_top=93.00
PASS  PEI top at bed_top                    PEI top z=93.00
PASS  all brackets touch the frame          11 brackets, floating: none
PASS  X rail centred on a beam slot         rail centre z=198.0, slots at 178.0, 198.0
PASS  interference is the known set only    7 found: 992 992 384 122 122 70 70
FAIL  timeline healthy                      1 unhealthy of 391
PASS  toolhead A parks clear of build area  nozzle x=110.0, build area 145.0..375.0
PASS  toolhead B parks clear of build area  nozzle x=410.0, build area 145.0..375.0
```

The single failure is the stale `Capture Position` entry, which is suppressed
and has no geometric effect.

### Parameter coverage, measured

The check that matters flexes each driving parameter and counts what actually
moved. The model is parametric only to the extent this number is high:

| Parameter | Followed | Pinned | Coverage |
|---|---:|---:|---:|
| `build_x` 230 → 300 | 6 | 52 | **10%** |
| `build_y` 235 → 305 | 7 | 50 | **12%** |
| `upright_h` 500 → 570 | 2 | 54 | **4%** |

So the honest figure is **4–12%**, not "parametric". Only the frame members
follow, because only they are rigid-jointed to the layout skeleton. Everything
added since sits at a fixed transform.

### The fix has a name

This is [skeletal modelling](https://help.autodesk.com/cloudhelp/2023/ENU/Inventor-Help/files/GUID-0435FE9D-6283-4CE0-813B-BD9B0BE5778C.htm),
Autodesk's own term for top-down design: one skeleton part carries the layout
sketches, datums and driving parameters, and every component references *only*
that skeleton. [Autodesk's large-assembly
guidance](https://help.autodesk.com/cloudhelp/2025/ENU/Inventor-Help/files/GUID-456388EE-9B7F-442E-B917-B76BDE016FD2.htm)
splits it per sub-assembly for anything this size, and the practitioner
consensus adds one rule worth stating plainly: **no sibling part may reference
another sibling** — shared interfaces are published through the skeleton.

The model already has the right bones. The `Layout` component is a skeleton; it
just stops at the frame. Extending it means a datum body per interface — X rail
seat, Y rail seats, Z rail seats, bed stack, each motor face — and a rigid joint
from every part to its datum instead of a baked transform.

Checked the Maker Store engineering wiki for prior art, since the team works in
Inventor. It has extrusion profile templates and file-naming and drawing
standards, but no skeleton or iLogic method to copy.

## 11. Still open

- The bed is still the slowest axis at 5,948 mm/s² against X's 13,259. Stiffer
  carrier bars are the next lever, at the cost of levelling-spacer height.
- Only the frame follows the parameters (§13).
- A stale `Capture Position` entry sits in the timeline, suppressed, with no
  geometric effect — every part measures where it should — but still flagged.
- **Parameter coverage is 4–12%** (§18). Converting the model to a full
  skeleton-driven assembly is the largest outstanding piece of work.
- The Z motor flange misses both slots on the top tie underside.
- The brackets are plain L-plates. They carry the right interfaces but have not
  been designed as printed or machined parts.
- Bed levelling hardware (springs or silicone spacers) is not modelled.
- Belt clamps where the belts meet the carriages are not modelled.
- Wiring and drag chain are not modelled.
- No printed part has been designed. The brackets in the model are plain plates
  standing in for parts that still have to be drawn, and the carriage and Z
  plates are solid rectangles that would really carry cutouts and hole patterns.
- `safe_distance` and the park positions are derived from the model, not measured.
- No source in Australia currently stocks the 235 × 235 24 V heated bed.
